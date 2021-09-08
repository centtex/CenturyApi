from flask import jsonify, request, Response
from models import db
from sqlalchemy.sql import text
from caching import CacheData
from firebase_wrap import FirebaseAuthenticate
from dateutil import parser

class PackingSlip:
    def __init__(self):
        self.cache = CacheData()

    def getPackingSlip(self, user_id):
        if request.method == 'POST':
            if FirebaseAuthenticate.get_user_token(user_id):

                request_data = request.get_json()
                if 'user_id' in request_data and 'packingslip_id' in request_data \
                        and 'from_date' in request_data \
                        and 'to_date' in request_data and 'cmp_code' in request_data \
                        and 'pagenumber' in request_data and 'pagesize' in request_data:

                    cached_data = self.cache.get_data('packingslip' + '-data')

                    if cached_data is None:
                        sql_stmt = "SELECT CMP_CODE,PACKINGSLIPID,SERIALNO,BALENO,VDATE,ORDERNO,ORDER_DATE,CONFNO" \
                                   ",CONF_DATE,PARTY,PARTYCITY,TRANSPORT_NAME,STATION,DETAILROWNO,ITEM_ID" \
                                   ",ITEM,PCS,MTRS,TOTAL,ROWNO,TP,DDSRNO,COLNO,ASSORT_PCS,ASS_SRNO,FLAG" \
                                   ",Narration,SCREEN,SELF_PARTY,OTHER,FOLDNO,LOTNO,LRNO,D_COLNO,PARTYID,AGENTID " \
                                   "FROM( SELECT PS.CMP_CODE,PS.PACKINGSLIPID,PS.SERIALNO,PS.BALENO" \
                                   ",PS.VCH_DATE AS VDATE,PS.ORDERNO,PS.ORDER_DATE" \
                                   ",PS.CONFNO,PS.CONF_DATE,PS.FOLDNO,PS.LOTNO,PS.LRNO,PS.D_COLNO" \
                                   ",PS.NARRATION,PS.SELF_PARTY,PS.OTHER, PS.Lgr_id AS PARTYID, PS.Agent_Id AS AGENTID" \
                                   ",PSD.DETAILROWNO,PSD.ITEM_ID,PSDD.PCS as PCS,PSDD.MTRS as MTRS" \
                                   ",PSDD.TOTAL as TOTAL,PSDD.ROWNO,PSDD.TP,PSDD.SRNO AS DDSRNO" \
                                   ",LM.LGR_NAME AS PARTY,PCM.CITY_NAME AS PARTYCITY,TM.TRANSPORT_NAME" \
                                   ",SCM.CITY_NAME AS STATION,IM.ITEM_NAME AS ITEM" \
                                   ",0 AS COLNO,0 AS ASSORT_PCS,0 AS ASS_SRNO,'D' AS FLAG" \
                                   ",SM.SCREEN_NAME AS SCREEN FROM packingslip PS " \
                                   "INNER JOIN packingslipdetail PSD ON PSD.PACKINGSLIPID=PS.PACKINGSLIPID " \
                                   "INNER JOIN packingslipdetaildetail PSDD ON PSDD.PACKINGSLIPID=PS.PACKINGSLIPID " \
                                   "AND PSDD.ROWNO=PSD.DETAILROWNO " \
                                   "INNER JOIN itemmaster IM ON IM.ITEM_ID=PSD.ITEM_ID " \
                                   "INNER JOIN screenmaster SM ON SM.SCREEN_ID=PSD.SCREEN_ID " \
                                   "INNER JOIN ledgermaster LM ON LM.LGR_ID=PS.LGR_ID " \
                                   "LEFT JOIN transportmaster TM ON TM.TRANSPORT_ID=PS.TRANSPORT_ID " \
                                   "LEFT JOIN citymaster PCM ON PCM.CITY_ID=LM.CITY_ID " \
                                   "LEFT JOIN citymaster SCM ON SCM.CITY_ID=PS.STATION_ID " \
                                   "WHERE PS.FLAG='C' UNION ALL " \
                                   "SELECT PS.CMP_CODE,PS.PACKINGSLIPID,PS.SERIALNO,PS.BALENO,PS.VCH_DATE AS DATE" \
                                   ",PS.ORDERNO,PS.ORDER_DATE,PS.CONFNO,PS.CONF_DATE" \
                                   ",PS.FOLDNO,PS.LOTNO,PS.LRNO,PS.D_COLNO,PS.NARRATION" \
                                   ",PS.SELF_PARTY,PS.OTHER,PS.Lgr_id AS PARTYID, PS.Agent_Id AS AGENTID" \
                                   ",PSD.DETAILROWNO,PSD.ITEM_ID" \
                                   ",0 as PCS,0 as MTRS,0 as TOTAL,0 as ROWNO,0 AS TP,0 AS DDSRNO" \
                                   ",LM.LGR_NAME AS PARTY,PCM.CITY_NAME AS PARTYCITY" \
                                   ",TM.TRANSPORT_NAME,SCM.CITY_NAME AS STATION,IM.ITEM_NAME AS ITEM" \
                                   ",0 AS COLNO,0 AS ASSORT_PCS,0 AS ASS_SRNO,'A' AS FLAG" \
                                   ",SM.SCREEN_NAME AS SCREEN FROM packingslip PS " \
                                   "INNER JOIN packingslipdetail PSD ON PSD.PACKINGSLIPID=PS.PACKINGSLIPID " \
                                   "INNER JOIN itemmaster IM ON IM.ITEM_ID=PSD.ITEM_ID " \
                                   "INNER JOIN screenmaster SM ON SM.SCREEN_ID=PSD.SCREEN_ID " \
                                   "INNER JOIN ledgermaster LM ON LM.LGR_ID=PS.LGR_ID " \
                                   "INNER JOIN transportmaster TM ON TM.TRANSPORT_ID=PS.TRANSPORT_ID " \
                                   "LEFT JOIN citymaster PCM ON PCM.CITY_ID=LM.CITY_ID " \
                                   "LEFT JOIN citymaster SCM ON SCM.CITY_ID=PS.STATION_ID " \
                                   "WHERE PS.FLAG='C') AS DETAIL WHERE CMP_CODE = %(cmpcode)s" \
                                   "" % {"cmpcode": request_data['cmp_code']}
                        sql_stmt += " ORDER BY BALENO,ITEM,DETAILROWNO,FLAG DESC,DDSRNO"
                        packing_slip_data = db.session.execute(text(sql_stmt), {"db": "classicmodels"})
                        cached_data = [slip._asdict() for slip in packing_slip_data.all()]
                        self.cache.set_data('packingslip' + '-data', cached_data)

                        # if request_data['user_id']:
                        #     ids_ = ', '.join(str(u) for u in request_data['user_id'])
                        #     sql_stmt += " AND PARTYID IN (%(userid)s) " % {"userid": ids_}
                        # if request_data['agent_id']:
                        #     sql_stmt += "AND AGENTID = %(agentid)s " % {"agentid": request_data['Agent_id']}
                        # if request_data['packingslip_id']:
                        #     sql_stmt += "AND PACKINGSLIPID = '%(packingslipid)s' " % {
                        #         "packingslipid": request_data['packingslip_id']}
                        # if request_data['from_date']:
                        #     sql_stmt += "AND VDATE >= '%(fromdate)s' " % {"fromdate": request_data['from_date']}
                        # if request_data['to_date']:
                        #     sql_stmt += "AND VDATE <= '%(todate)s' " % {"todate": request_data['to_date']}

                    if request_data['user_id']:
                        # ids_ = ', '.join(str(u) for u in request_data['user_id'])
                        cached_data = [d for d in cached_data if d['PARTYID'] in request_data['user_id']]

                    if request_data['agent_id']:
                        cached_data = [d for d in cached_data if d['AGENTID'] == request_data['agent_id']]

                    if request_data['packingslip_id']:
                        cached_data = [d for d in cached_data if d['BALENO'] == request_data['packingslip_id']]

                    if request_data['from_date']:
                        from_date = parser.parse(request_data['from_date'])
                        cached_data = list(filter(lambda x: x['VDATE'] >= from_date, cached_data))

                    if request_data['to_date']:
                        to_date = parser.parse(request_data['to_date'])
                        cached_data = list(filter(lambda x: x['VDATE'] <= to_date, cached_data))

                    page_number = request_data['pagenumber']
                    page_size = request_data['pagesize']

                    start_index = 0

                    if page_number >= 1 and page_size != 0 and page_size < len(cached_data):
                        start_index = page_size * (page_number - 1)
                        end_index = (page_size * page_number)
                    else:
                        end_index = len(cached_data)

                    return jsonify(cached_data[start_index:end_index])
                else:
                    return Response(
                        "Invalid Request Object",
                        status=400,
                    )
            else:
                return Response(
                    "User Not Authorized",
                    status=404,
                )
        else:
            return Response(
                "Invalid Request",
                status=400,
            )
