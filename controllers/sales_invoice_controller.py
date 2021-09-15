from flask import jsonify, request, Response
from models import db
from sqlalchemy.sql import text
from caching import CacheData
from dateutil import parser
from firebase_wrap import FirebaseAuthenticate
from common.helper import Helper

from time import time


class SalesInvoiceController:
    def __init__(self):
        self.cache = CacheData()
        self.helper = Helper()

    def getInvoiceDetails(self, user_id):
        if request.method == 'POST':
            if FirebaseAuthenticate.get_user_token(user_id):
                request_data = request.get_json()
                if 'cmp_code' in request_data and 'user_id' in request_data and \
                        'invoice_id' in request_data and 'from_date' in request_data \
                        and 'to_date' in request_data and 'agent_id' in request_data \
                        and 'pagenumber' in request_data and 'pagesize' in request_data:

                    cached_data = self.cache.get_data('invoice' + '-data')
                    if cached_data is None:
                        start = time()
                        sql_stmt = "SELECT INVD.*, INVD.SIGNED_QR_CODE,HM.HSN_NAME AS HSNCODE FROM (" \
                                   "SELECT INV.*,IM.HSN_ID,UPPER(PCM.city_name) AS PARTY_CITY" \
                                   ",UPPER(PSM.state_name) AS PARTY_STATE,UPPER(ACM.CITY_NAME) AS AGENT_CITY" \
                                   ",COCM.CITY_NAME AS CONSIGNEE_CITY,COSM.STATE_NAME AS CONSIGNEE_STATE" \
                                   ",COSM.State_Code AS CONSIGNEE_STATECODE,PRI.PRICE_NAME,SCM.SCREEN_NAME" \
                                   ",IM.ITEM_NAME,UM.UNIT_NAME FROM (SELECT SI.SIGNED_QR_CODE,SI.SAL_INV_ID" \
                                   ",SI.Lgr_Id AS PARTY_ID,SI.AGENT_ID,SID.Item_Id,SID.SCREEN_ID,SID.UNIT_ID" \
                                   ",LM.City_Id AS PARTY_CITY_ID,LM.STATE_ID AS PARTY_STATE_ID" \
                                   ",AGM.City_Id AS AGENT_CITY_ID,CMM.City_Id,CMM.STATE_ID,SO.PRICE_ID" \
                                   ",SI.IRN,SI.EINVNO AS AKN_NO,SI.ACK_DATE AS AKN_DATE" \
                                   ",SI.SAL_INV_BILL_NO AS BILLNO,SI.SAL_INV_VDATE AS INV_DATE" \
                                   ",SI.ORDERNO,SI.ORDERDATE,SI.SAL_INV_LRNO as LRNO,SI.SAL_INV_LRDATE AS LRDATE" \
                                   ",SI.EWB_DATE AS EWAY_BILL_DATE,IFNULL(SI.EWAYBILLNO,'') AS EWAY_BILLNO" \
                                   ",SI.CONFNO,SI.CONFDATE,SI.WEIGHT,SI.FREIGHT,SI.SAL_INV_ADD1,SI.SAL_INV_ADD2" \
                                   ",SI.SAL_INV_ADD3,SI.SAL_INV_ADD4,SI.SAL_INV_ADD5,SI.SAL_INV_ADDTOTAL" \
                                   ",SI.Sal_Inv_Add1_Set,SI.Sal_Inv_Add2_Set,SI.Sal_Inv_Add3_Set" \
                                   ",SI.Sal_Inv_Add4_Set,SI.Sal_Inv_Add5_Set,SI.SAL_INV_LESS1,SI.SAL_INV_LESS2" \
                                   ",SI.SAL_INV_LESS3,SI.SAL_INV_LESS4,SI.SAL_INV_LESS5,SI.SAL_INV_LESSTOTAL" \
                                   ",SI.Sal_Inv_Less1_Set,SI.Sal_Inv_Less2_Set,SI.Sal_Inv_Less3_Set" \
                                   ",SI.Sal_Inv_Less4_Set,SI.Sal_Inv_Less5_Set,IFNULL(SI.TCS_PER,0) AS TCS_PER" \
                                   ",SI.TCS_AMT,(SI.SAL_INV_ADD1+SI.SAL_INV_ADD2) AS ADDBEFOREVALUE" \
                                   ",(SI.Sal_Inv_GrossTotal-SI.Sal_Inv_LessTotal+(SI.SAL_INV_ADD1+SI.SAL_INV_ADD2))" \
                                   " AS TAXABLEAMT,SI.SAL_INV_GROSSTOTAL,SI.Sal_Inv_PcsTotal" \
                                   ",SI.Sal_Inv_BalesTotal,SI.Sal_Inv_QuantityTotal,SI.Sal_Inv_NetQuantityTotal" \
                                   ",SI.SAL_INV_NETTOTAL AS NET_TOTAL_AMOUNT,SI.SAL_INV_ROUNDOFF" \
                                   ",SI.NET_SNET AS ITEM_NET_SNET,SI.AMT_WORD AS AMOUNT_IN_WORDS" \
                                   ",UPPER(SI.DOCUMENTS) AS THROUGH,SID.SERIALNO,SID.SAL_INV_BALENO AS BALENO" \
                                   ",SID.ITEM_CUT AS FOLD,SID.SAL_INV_PCS AS ITEM_PCS,SID.SAL_INV_QTY" \
                                   ",SID.SAL_INV_AMOUNT AS AMOUNT,SID.SAL_INV_RATE AS ITEM_RATE" \
                                   ",SID.DESCRIPTION AS INVOICE_DESCRIPTION,SID.NETQTY AS ITEM_NET_MTR_QTY" \
                                   ",SI.party_statecode AS PARTY_STATE_CODE,UPPER(LM.LGR_NAME) AS PARTY_NAME" \
                                   ",UPPER(LM.LGR_ADD1) AS PARTY_ADD1,UPPER(LM.LGR_ADD2) AS PARTY_ADD2" \
                                   ",UPPER(LM.LGR_ADD3) AS PARTY_ADD3,LM.CITY_PINCODE AS PARTY_PINCODE" \
                                   ",LM.GSTINNO AS PARTY_GSTINNO,LM.ADHARNO AS PARTY_AADHARNO" \
                                   ",LM.Lgr_Pano AS PARTY_PAN_NO,LM.IECODE,UPPER(AGM.LGR_NAME) AS BROKER" \
                                   ",SO.SCHEME,SO.SCHEME_PER,CMM.Name AS CONSIGNEE_NAME,CMM.Add1 AS CONSIGNEE_ADD1" \
                                   ",CMM.Add2 AS CONSIGNEE_ADD2,CMM.Add3 AS CONSIGNEE_ADD3" \
                                   ",CMM.GSTINNO AS CONSIGNEE_GSTNO,CMM.PhoneNo AS CONSIGNEE_PHONE" \
                                   ",CMM.MobileNo AS CONSINGEE_MOBILE,CU.CourierMaster_Name AS COURIER_NAME" \
                                   ",TM.TRANSPORT_NAME,CM.CITY_NAME AS DISPATCHED_BY FROM salesinvoice SI " \
                                   "LEFT JOIN salesinvoicedetail SID ON SID.SAL_INV_ID=SI.SAL_INV_ID " \
                                   "LEFT JOIN salesorder SO ON SO.CONFNO <=> SI.CONFNO " \
                                   "LEFT JOIN ledgermaster LM ON LM.LGR_ID<=>SI.LGR_ID " \
                                   "LEFT JOIN ledgermaster AGM ON AGM.LGR_ID<=>SI.AGENT_ID " \
                                   "LEFT JOIN couriermaster CU ON CU.COURIERMASTER_ID<=>SI.COURIERMASTER_ID " \
                                   "LEFT JOIN transportmaster TM ON TM.TRANSPORT_ID<=>SI.TRANSPORT_ID " \
                                   "LEFT JOIN consigneemaster CMM ON CMM.Consignee_Id<=>SI.Consignee_Id " \
                                   "LEFT JOIN citymaster CM ON CM.CITY_ID<=>SI.STATION_ID " \
                                   "where SI.CMP_CODE = %(cmpcode)s AND SO.CMP_CODE = %(cmpcode)s) INV " \
                                   "LEFT JOIN pricelist PRI ON PRI.PRICE_ID <=> INV.PRICE_ID " \
                                   "AND PRI.ITEM_ID <=> INV.Item_Id " \
                                   "LEFT JOIN screenmaster SCM ON SCM.SCREEN_ID<=>INV.SCREEN_ID " \
                                   "LEFT JOIN itemmaster IM ON IM.ITEM_ID<=>INV.ITEM_ID " \
                                   "LEFT JOIN unitmaster UM ON UM.UNIT_ID=INV.UNIT_ID " \
                                   "LEFT JOIN citymaster PCM ON PCM.CITY_ID<=>INV.PARTY_CITY_ID " \
                                   "LEFT JOIN statemaster PSM ON PSM.STATE_ID <=> INV.PARTY_STATE_ID " \
                                   "LEFT JOIN citymaster ACM ON ACM.CITY_ID<=>INV.AGENT_CITY_ID " \
                                   "LEFT JOIN citymaster COCM ON COCM.CITY_ID<=>INV.City_Id " \
                                   "LEFT JOIN statemaster COSM ON COSM.STATE_ID <=> INV.STATE_ID) INVD " \
                                   "LEFT JOIN hsnmaster HM ON HM.HSN_ID<=>INVD.HSN_ID" \
                                   % {"cmpcode": request_data['cmp_code']}

                        invoice_data = db.session.execute(text(sql_stmt), {"db": "classicmodels"})
                        print(" time taken to execute ", time() - start)
                        cached_data = [invoice._asdict() for invoice in invoice_data.all()]

                        for data in cached_data:
                            del data['SAL_INV_ID']
                            del data['Item_Id']
                            del data['SCREEN_ID']
                            del data['UNIT_ID']
                            del data['PARTY_CITY_ID']
                            del data['PARTY_STATE_ID']
                            del data['AGENT_CITY_ID']
                            del data['City_Id']
                            del data['STATE_ID']
                            del data['PRICE_ID']

                        self.cache.set_data('invoice' + '-data', cached_data)

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

                    if request_data['invoice_id']:
                        cached_data = [d for d in cached_data if d['BILLNO'] == int(request_data['invoice_id'])]

                    if request_data['from_date']:
                        from_date = parser.parse(request_data['from_date'])
                        cached_data = list(filter(lambda x: x['VDATE'] >= from_date, cached_data))

                    if request_data['to_date']:
                        to_date = parser.parse(request_data['to_date'])
                        cached_data = list(filter(lambda x: x['VDATE'] <= to_date, cached_data))

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
            return Response(
                "Invalid Request",
                status=400,
            )
