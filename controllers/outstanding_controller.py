from flask import jsonify, request, Response
from models import db
from sqlalchemy.sql import text
from caching import CacheData
from dateutil import parser
from firebase_wrap import FirebaseAuthenticate
from common.helper import Helper


class OutStandingController:
    def __init__(self):
        self.cache = CacheData()
        self.helper = Helper()

    def getOutStandingDetails(self, user_id):
        if request.method == 'POST':
            if FirebaseAuthenticate.get_user_token(user_id):
                request_data = request.get_json()
                if 'cmp_code' in request_data and 'user_id' in request_data \
                        and 'from_date' in request_data and 'to_date' in request_data \
                        and 'agent_id' in request_data \
                        and 'pagenumber' in request_data and 'pagesize' in request_data:

                    cached_data = self.cache.get_data('outstanding' + '-data')
                    if cached_data is None:
                        sql_stmt = "SELECT * FROM (SELECT PD.BILL_NO AS BILLNO,PD.DATE as BILLDATE" \
                                   ",AJ.RecDate,PD.Lgr_ID AS PARTYID,PD.AGENT_ID AS AGENTID,PD.LrNo" \
                                   ",PD.LrDate,PD.VCODE AS VCODE,PD.BILL_AMOUNT,PD.REC_AMOUNT" \
                                   ",(PD.BILL_AMOUNT + SUM(IFNULL(AJ.INTEREST ,0)))-(SUM(IFNULL(AJ.ADJUSTAMT ,0))" \
                                   "+SUM(IFNULL(AJ.TOTAL ,0))+SUM(IFNULL(AJ.INTREC ,0))) AS PENDINGAMOUNT" \
                                   ",0 AS PARTAMOUNT,PD.Discount,PD.Interest,LM.LGR_NAME AS PARTY" \
                                   ",ALM.LGR_NAME AS AGENT,PD.JOBFLAG,DATEDIFF(CURDATE(),PD.DATE) as OUTDAYS" \
                                   ",PD.Cmp_Code AS CMP_CODE FROM partydetail PD " \
                                   "LEFT JOIN adjmaster AJ ON AJ.BILLNO=PD.BILL_NO AND AJ.FLAG=PD.JOBFLAG " \
                                   "AND AJ.CMP_CODE=PD.CMP_CODE AND PD.VCODE=AJ.VCODE " \
                                   "left join ledgermaster LM on LM.Lgr_ID=PD.Lgr_ID " \
                                   "left join ledgermaster ALM on ALM.Lgr_ID=PD.Agent_ID " \
                                   "WHERE PD.JobFlag = 'S' " \
                                   "GROUP BY PD.BILL_NO,PD.DATE,AJ.RecDate,PD.VCODE,PD.REC_AMOUNT,PD.Discount" \
                                   ",PD.Interest,PD.BILL_AMOUNT,LM.LGR_NAME ,ALM.LGR_NAME," \
                                   "PARTYID, AGENTID, CMP_CODE, PD.LrNo, PD.LrDate " \
                                   "UNION ALL " \
                                   "SELECT TM.TRAN_DOCNO AS BILLNO,TM.Tran_Date AS BILLDATE,null as RecDate" \
                                   ",TD.Tran_Detail_ID AS PARTYID,LD.Agent_Id AS AGENTID,'' AS LrNo" \
                                   ",NULL AS LrDate,TM.TRAN_ID as VCode,0 AS BILL_AMOUNT,0 AS REC_AMOUNT" \
                                   ",0 AS PENDINGAMOUNT,(CASE WHEN TD.TRAN_TYPE='J' THEN " \
                                   "(case when TD.Tran_DrCr='C' then " \
                                   "TD.PartAmount ELSE 0 END) WHEN TD.TRAN_TYPE='DN' THEN (case when TD.Tran_DrCr='C' " \
                                   "THEN TD.PartAmount ELSE 0 END) ELSE (case when TD.Tran_DrCr='C' " \
                                   "THEN TD.PartAmount ELSE 0 END) END) as PartAmount,0 AS Discount,0 AS Interest" \
                                   ",LM.Lgr_Name as Party,ALM.Lgr_Name as Agent,TM.TRAN_TYPE as JobFlag" \
                                   ",DATEDIFF(CURDATE(),TM.Tran_Date) as OUTDAYS,TD.Cmp_Code AS CMP_CODE " \
                                   "from trandetail TD inner join tranmaster TM on TM.Tran_ID=TD.Tran_ID and " \
                                   "TM.Tran_Type=TD.Tran_Type and TD.Cmp_Code=TM.Cmp_Code " \
                                   "inner join ledgermaster LM on LM.Lgr_ID=TD.Tran_Detail_ID " \
                                   "left join ledgerdetail LD on LM.Lgr_ID=LD.Lgr_ID and TD.Cmp_Code=LD.Cmp_Code " \
                                   "left join ledgermaster ALM on ALM.Lgr_Id=LD.Agent_ID where " \
                                   "(case when TD.Tran_DrCr='C' then (TD.PartAmount) else 0 end) <>0 and " \
                                   "TD.ShowPartAmt=1 and TD.Tran_Type='BR' and (TD.REC_TRANS=0 OR TD.REC_TRANS IS NULL)" \
                                   ") OS WHERE CMP_CODE = %(cmpcode)s " % {"cmpcode": request_data['cmp_code']}
                        sql_stmt += "ORDER BY BILLDATE DESC"
                        outstanding_data = db.session.execute(text(sql_stmt), {"db": "classicmodels"})
                        cached_data = [outstanding._asdict() for outstanding in outstanding_data.all()]
                        self.cache.set_data('outstanding' + '-data', cached_data)

                    if request_data['user_id']:
                        check = self.helper.check_if_user_id_exist(user_id, request_data['user_id'])
                        if check:
                            cached_data = [d for d in cached_data if d['PARTYID'] in request_data['user_id']]
                        else:
                            return Response(
                                "User Is Not Authorized to access other user data",
                                status=404,
                            )

                    if request_data['agent_id']:
                        cached_data = [d for d in cached_data if d['AGENTID'] == request_data['agent_id']]

                    if request_data['from_date']:
                        from_date = parser.parse(request_data['from_date'])
                        cached_data = list(filter(lambda x: x['BILLDATE'] >= from_date, cached_data))

                    if request_data['to_date']:
                        to_date = parser.parse(request_data['to_date'])
                        cached_data = list(filter(lambda x: x['BILLDATE'] <= to_date, cached_data))

                    page_number = request_data['pagenumber']
                    page_size = request_data['pagesize']

                    if len(cached_data) < page_size and page_number > 1:
                        return jsonify([])
                    else:
                        start_index = 0
                        if page_number >= 1 and page_size != 0 and page_size < len(cached_data):
                            start_index = page_size * (page_number - 1)
                            end_index = (page_size * page_number)
                        else:
                            end_index = len(cached_data)

                        return jsonify(cached_data[start_index:end_index])
                else:
                    return Response("Invalid Request Object", status=400)
            else:
                return Response("User Not Authorized", status=404)
        else:
            return Response("Invalid Request", status=400)
