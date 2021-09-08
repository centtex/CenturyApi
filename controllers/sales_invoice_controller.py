from flask import jsonify, request, Response
from models import db
from sqlalchemy.sql import text
from caching import CacheData
from dateutil import parser
from firebase_wrap import FirebaseAuthenticate


class SalesInvoiceController:
    def __init__(self):
        self.cache = CacheData()

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
                        sql_stmt = "SELECT INVD.CMP_CODE,INVD.SAL_INV_ID,INVD.PARTYID,INVD.AGENTID" \
                                   ",INVD.ACK_DATE AS AKN_DATE,INVD.ADDBEFOREVALUE" \
                                   ",INVD.ADHARNO AS AADHAR_NO,INVD.AGENTCITY,INVD.BROKER,INVD.ALIAS" \
                                   ",INVD.AMOUNT,INVD.AMT_WORD as AMOUNT_IN_WORDS,INVD.BALENO" \
                                   ",INVD.BILLNO,INVD.CITY_PINCODE AS PARTY_PINCODE" \
                                   ",INVD.cmp_ServiceTax_No AS COMPANY_CIN_NO,INVD.COMPANY_NAME" \
                                   ",INVD.COMPANY_TIN_NO,INVD.COMPANY_PAN_NO,INVD.COMPANY_JURISDICTION" \
                                   ",INVD.COMPANY_ADD1,INVD.COMPANY_ADD2,INVD.COMPANY_CITY" \
                                   ",INVD.COMPANY_STATE,INVD.COMPANY_EMAIL,INVD.COMPANY_PHONE1" \
                                   ",INVD.COMPANY_PHONE2,INVD.COMPANY_MOBILE,INVD.COMPANY_ACC_NO_1" \
                                   ",INVD.COMPANY_ACC_NO_2,INVD.COMPANY_ACC_NO_3" \
                                   ",INVD.CMP_INTERESTRATE AS INTEREST_PER_DAY,INVD.COMPANY_GSTIN_NO" \
                                   ",INVD.CONFDATE,INVD.CONFNO,INVD.CONSIGNEENAME,INVD.CONSIGNEE_ADD1" \
                                   ",INVD.CONSIGNEE_ADD2,INVD.CONSIGNEE_ADD3,INVD.CONSIGNEE_CITY" \
                                   ",INVD.CONSIGNEE_COUNTRY,INVD.CONSIGNEE_GSTNO,INVD.CONSIGNEE_STATE" \
                                   ",INVD.CONSINGEE_MOBILE,INVD.CourierMaster_Name,INVD.INVOICE_DESCRIPTION" \
                                   ",INVD.THROUGH,INVD.EWAYBILLNO,INVD.EWB_DATE AS EWAY_BILL_DATE" \
                                   ",INVD.EXPORTTYPE,INVD.FREIGHT,INVD.GSTINNO AS PARTY_GSTINNO,INVD.IRN" \
                                   ",INVD.ITEM_NAME,INVD.ITEM_CUT AS FOLD,INVD.LGRBRANCH AS PARTY_BRANCH" \
                                   ",INVD.LGR_ADD1 AS PARTY_ADD1,INVD.LGR_ADD2 AS PARTY_ADD2" \
                                   ",INVD.LGR_ADD3 AS PARTY_ADD3,INVD.LGR_BANK AS PARTY_BANK" \
                                   ",INVD.LGR_INTERESTRATE AS PARTY_INTEREST_RATE" \
                                   ",INVD.Lgr_Pano AS PARTY_PAN_NO,INVD.NETQTY AS ITEM_NET_MTR_QTY" \
                                   ",INVD.SAL_INV_NETTOTAL AS NET_TOTAL_AMOUNT,INVD.NET_SNET AS ITEM_NET_SNET" \
                                   ",INVD.ORDERDATE,INVD.ORDERNO,INVD.PARTYCITY,INVD.PARTYNAME" \
                                   ",INVD.PCS AS ITEM_PCS,INVD.PRICE_NAME,INVD.QR_CODE" \
                                   ",INVD.QUANTITY AS ITEM_QTY_MTR_KG,INVD.RATE AS ITEM_RATE,INVD.REMARK" \
                                   ",INVD.SAL_INV_ADD1,INVD.SAL_INV_ADD2,INVD.SAL_INV_ADD3,INVD.SAL_INV_ADD4" \
                                   ",INVD.SAL_INV_ADD5,INVD.SAL_INV_ADDTOTAL,INVD.SAL_INV_DAYS" \
                                   ",INVD.SAL_INV_GROSSTOTAL,INVD.SAL_INV_LESS1,INVD.SAL_INV_LESS2" \
                                   ",INVD.SAL_INV_LESS3,INVD.SAL_INV_LESS4,INVD.SAL_INV_LESS5" \
                                   ",INVD.SAL_INV_LESSTOTAL,INVD.SAL_INV_LRDATE AS LRDATE" \
                                   ",INVD.SAL_INV_LRNO AS LRNO,INVD.SAL_INV_ROUNDOFF,INVD.Sal_Inv_PcsTotal" \
                                   ",INVD.Sal_Inv_BalesTotal,INVD.Sal_Inv_QuantityTotal" \
                                   ",INVD.Sal_Inv_NetQuantityTotal,INVD.SCHEME,INVD.SCHEME_PER,INVD.SCREEN_NAME" \
                                   ",INVD.SERIALNO,INVD.Sal_Inv_Add1_Set,INVD.Sal_Inv_Add2_Set" \
                                   ",INVD.Sal_Inv_Add3_Set,INVD.Sal_Inv_Add4_Set,INVD.Sal_Inv_Add5_Set" \
                                   ",INVD.Sal_Inv_Less1_Set,INVD.Sal_Inv_Less2_Set,INVD.Sal_Inv_Less3_Set" \
                                   ",INVD.Sal_Inv_Less4_Set,INVD.Sal_Inv_Less5_Set,INVD.TAXABLEAMT,INVD.TCS_AMT" \
                                   ",INVD.TCS_PER,INVD.TRANSPORT_NAME,INVD.UNIT_NAME,INVD.VDATE,INVD.WEIGHT" \
                                   ",INVD.consingee_phone,HM.HSN_NAME AS HSNCODE" \
                                   ",UPPER(SM.STATE_NAME) AS PARTYSTATE,INVD.DISPATCHED_BY FROM (SELECT INV.*" \
                                   ",UPPER(PCM.CITY_NAME) AS PARTYCITY,IM.ITEM_NAME,SCM.SCREEN_NAME" \
                                   ",PCM.STATE_ID,UPPER(ACM.CITY_NAME) AS AGENTCITY,UM.UNIT_NAME" \
                                   ",IM.HSN_ID,COCM.CITY_NAME AS CONSIGNEE_CITY" \
                                   ",COSM.STATE_NAME AS CONSIGNEE_STATE,COSM.State_Code AS CONSIGNEE_STATECODE" \
                                   ",STCM.CITY_NAME AS DISPATCHED_BY " \
                                   "FROM (SELECT SI.SAL_INV_ID,TO_BASE64(SI.SIGNED_QR_CODE) as QR_CODE" \
                                   ",SI.SAL_INV_BILL_NO AS BILLNO,SI.SALES_ALIAS AS ALIAS" \
                                   ",SI.SAL_INV_VDATE AS VDATE,SI.ORDERNO,SI.ORDERDATE,SI.SAL_INV_LRNO" \
                                   ",SI.SAL_INV_LRDATE,SI.SAL_INV_ADD1,SI.SAL_INV_ADD2,SI.SAL_INV_ADD3" \
                                   ",SI.SAL_INV_ADD4,SI.SAL_INV_ADD5,SI.SAL_INV_LESS1,SI.SAL_INV_LESS2" \
                                   ",SI.SAL_INV_LESS3,SI.SAL_INV_LESS4,SI.SAL_INV_LESS5,SI.SAL_INV_ADDTOTAL" \
                                   ",SI.Sal_Inv_PcsTotal,SI.Sal_Inv_BalesTotal,SI.Sal_Inv_QuantityTotal" \
                                   ",SI.Sal_Inv_NetQuantityTotal" \
                                   ",SAL_INV_ROUNDOFF,SI.SAL_INV_LESSTOTAL,SI.SAL_INV_GROSSTOTAL" \
                                   ",SI.SAL_INV_DAYS,SI.NET_SNET,SI.WEIGHT,SI.FREIGHT,SI.CONFNO" \
                                   ",SI.CONFDATE,SI.LGR_BANK,IFNULL(SI.SAL_REMARK,'') AS REMARK,SI.AMT_WORD" \
                                   ",IFNULL(SI.Sal_Inv_Less1_Set,0) AS Sal_Inv_Less1_Set" \
                                   ",IFNULL(SI.Sal_Inv_Less2_Set,0) AS Sal_Inv_Less2_Set" \
                                   ",IFNULL(SI.Sal_Inv_Less3_Set,0) AS Sal_Inv_Less3_Set" \
                                   ",IFNULL(SI.Sal_Inv_Less4_Set,0) AS Sal_Inv_Less4_Set" \
                                   ",IFNULL(SI.Sal_Inv_Less5_Set,0) AS Sal_Inv_Less5_Set" \
                                   ",UPPER(SI.DOCUMENTS) AS THROUGH,UPPER(SI.OUR_BRANCH) AS OURBRANCH" \
                                   ",UPPER(SI.LGR_BRANCH) AS LGRBRANCH" \
                                   ",IFNULL(SI.Sal_Inv_Add1_Set,0)Sal_Inv_Add1_Set" \
                                   ",IFNULL(SI.Sal_Inv_Add2_Set,0)Sal_Inv_Add2_Set" \
                                   ",IFNULL(SI.Sal_Inv_Add3_Set,0)Sal_Inv_Add3_Set" \
                                   ",IFNULL(SI.Sal_Inv_Add4_Set,0)Sal_Inv_Add4_Set" \
                                   ",IFNULL(SI.Sal_Inv_Add5_Set,0)Sal_Inv_Add5_Set" \
                                   ",(SI.SAL_INV_ADD1+SI.SAL_INV_ADD2) AS ADDBEFOREVALUE" \
                                   ",(SI.Sal_Inv_GrossTotal-SI.Sal_Inv_LessTotal+(SI.SAL_INV_ADD1+SI.SAL_INV_ADD2)) AS TAXABLEAMT" \
                                   ",IFNULL(SI.EWAYBILLNO,'') AS EWAYBILLNO" \
                                   ",SI.EWB_DATE,SI.EXPORTTYPE,IFNULL(SI.TCS_PER,0) TCS_PER,IFNULL(SI.TCS_AMT,0) TCS_AMT" \
                                   ",SI.CMP_CODE,SI.IRN,SI.ACK_DATE,SI.SAL_INV_NETTOTAL" \
                                   ",SI.Lgr_Id AS PARTYID,SI.AGENT_ID AS AGENTID" \
                                   ",SID.SAL_INV_BALENO AS BALENO,SID.ITEM_CUT,SID.SAL_INV_PCS AS PCS" \
                                   ",SID.SAL_INV_QTY AS QUANTITY,SID.SAL_INV_AMOUNT AS AMOUNT" \
                                   ",SID.SAL_INV_RATE AS RATE,SID.SERIALNO,IFNULL(SID.DESCRIPTION,'') " \
                                   "AS INVOICE_DESCRIPTION,SID.NETQTY, SID.UNIT_ID, SID.SCREEN_ID, SID.ITEM_ID" \
                                   ",UPPER(LM.LGR_NAME) AS PARTYNAME" \
                                   ",UPPER(LM.LGR_ADD1) AS LGR_ADD1,UPPER(LM.LGR_ADD2) AS LGR_ADD2" \
                                   ",UPPER(LM.LGR_ADD3)AS LGR_ADD3,LM.CITY_PINCODE,LM.GSTINNO" \
                                   ",LM.ADHARNO,LM.Lgr_Pano,IFNULL(LM.LGR_INTERESTRATE,0) AS LGR_INTERESTRATE" \
                                   ",LM.IECODE, LM.CITY_ID AS PARTYCITYID" \
                                   ",UPPER(AGM.LGR_NAME) AS BROKER, AGM.City_Id AS AGENTCITYID" \
                                   ",CMP.cmp_ServiceTax_No" \
                                   ",UPPER(CMP.CMP_NAME) AS COMPANY_NAME,CMP.CMP_TIN_NO AS COMPANY_TIN_NO" \
                                   ",CMP.CMP_PAN_NO AS COMPANY_PAN_NO" \
                                   ",CMP.CMP_JURISDICTION AS COMPANY_JURISDICTION" \
                                   ",IFNULL(CMP.CMP_ADD1,'') AS COMPANY_ADD1" \
                                   ",IFNULL(CMP.CMP_ADD2,'')AS COMPANY_ADD2" \
                                   ",IFNULL(CMP.CMP_CITY,'') AS COMPANY_CITY" \
                                   ",IFNULL(CMP.CMP_STATE,'') AS COMPANY_STATE" \
                                   ",IFNULL(CMP.BINNO,'') AS COMPANY_BINNO" \
                                   ",CMP.cmp_Email AS COMPANY_EMAIL,CMP.CMP_PHONE1 AS COMPANY_PHONE1" \
                                   ",CMP.CMP_PHONE2 AS COMPANY_PHONE2,CMP.CMP_MOBILE AS COMPANY_MOBILE" \
                                   ",CMP.CMP_BANK_ACCNO1 AS COMPANY_ACC_NO_1" \
                                   ",CMP.CMP_BANK_ACCNO2 AS COMPANY_ACC_NO_2" \
                                   ",CMP.CMP_BANK_ACCNO3 AS COMPANY_ACC_NO_3" \
                                   ",IFNULL(CMP.CMP_INTERESTRATE,0) AS CMP_INTERESTRATE" \
                                   ",CMP.GSTINNO  AS COMPANY_GSTIN_NO,SO.SCHEME,SO.SCHEME_PER" \
                                   ",CU.CourierMaster_Name" \
                                   ",IFNULL(CMM.Name,'C') AS CONSIGNEENAME,CMM.Add1 AS CONSIGNEE_ADD1" \
                                   ",CMM.Add2 AS CONSIGNEE_ADD2,CMM.Add3 AS CONSIGNEE_ADD3" \
                                   ",CMM.GSTINNO AS CONSIGNEE_GSTNO,CMM.PhoneNo AS consingee_phone" \
                                   ",CMM.MobileNo AS CONSINGEE_MOBILE,CMM.Contry AS CONSIGNEE_COUNTRY" \
                                   ",CMM.City_Id AS CONSCITYID, CMM.STATE_ID as CONSSTATEID" \
                                   ",P_DETAIL.PRICE_NAME,TM.TRANSPORT_NAME FROM salesinvoice SI " \
                                   "LEFT JOIN salesinvoicedetail SID ON SID.SAL_INV_ID=SI.SAL_INV_ID " \
                                   "LEFT JOIN ledgermaster LM ON LM.LGR_ID<=>SI.LGR_ID " \
                                   "LEFT JOIN ledgermaster AGM ON AGM.LGR_ID<=>SI.AGENT_ID " \
                                   "LEFT JOIN companymaster CMP ON CMP.CMP_CODE<=>SI.CMP_CODE " \
                                   "LEFT JOIN salesorder SO ON SO.CONFNO <=> SI.CONFNO AND SO.FYEAR <=> SI.SAL_FYEAR " \
                                   "LEFT JOIN citymaster CM ON CM.CITY_ID<=>SI.STATION_ID " \
                                   "LEFT JOIN consigneemaster CMM ON CMM.Consignee_Id<=>SI.Consignee_Id " \
                                   "LEFT JOIN couriermaster CU ON CU.COURIERMASTER_ID<=>SI.COURIERMASTER_ID " \
                                   "LEFT JOIN transportmaster TM ON TM.TRANSPORT_ID<=>SI.TRANSPORT_ID " \
                                   "LEFT JOIN (SELECT DISTINCT PRI.PRICE_NAME,SAI.SAL_INV_ID,SAI.CMP_CODE " \
                                   "FROM salesinvoice SAI " \
                                   "INNER JOIN salesorder SO ON SO.CONFNO <=> SAI.CONFNO AND " \
                                   "SO.FYEAR <=> SAI.SAL_FYEAR " \
                                   "LEFT JOIN pricelist PRI ON PRI.PRICE_ID <=> SO.PRICE_ID " \
                                   "WHERE SAI.CMP_CODE  =1 AND PRI.CMP_CODE = 1) AS P_DETAIL " \
                                   "ON P_DETAIL.SAL_INV_ID <=> SI.SAL_INV_ID AND P_DETAIL.CMP_CODE <=> SI.CMP_CODE " \
                                   ") as INV INNER JOIN screenmaster SCM ON SCM.SCREEN_ID<=>INV.SCREEN_ID " \
                                   "INNER JOIN itemmaster IM ON IM.ITEM_ID<=>INV.ITEM_ID " \
                                   "INNER JOIN unitmaster UM ON UM.UNIT_ID=INV.UNIT_ID " \
                                   "LEFT JOIN citymaster PCM ON PCM.CITY_ID<=>INV.PARTYCITYID " \
                                   "LEFT JOIN citymaster ACM ON ACM.CITY_ID<=>INV.AGENTCITYID " \
                                   "LEFT JOIN statemaster COSM ON COSM.STATE_ID <=> INV.CONSSTATEID " \
                                   "LEFT JOIN citymaster STCM ON STCM.CITY_ID<=>INV.STATION_ID " \
                                   "LEFT JOIN citymaster COCM ON COCM.CITY_ID<=>INV.CONSCITYID) AS INVD " \
                                   "LEFT JOIN hsnmaster HM ON HM.HSN_ID<=>INVD.HSN_ID " \
                                   "LEFT JOIN statemaster SM ON SM.STATE_ID<=>INVD.STATE_ID " \
                                   "where INVD.CMP_CODE = %(cmpcode)s" % {"cmpcode": request_data['cmp_code']}

                        invoice_data = db.session.execute(text(sql_stmt), {"db": "classicmodels"})
                        cached_data = [invoice._asdict() for invoice in invoice_data.all()]
                        self.cache.set_data('invoice' + '-data', cached_data)

                    if request_data['user_id']:
                        # ids_ = ', '.join(str(u) for u in request_data['user_id'])
                        cached_data = [d for d in cached_data if d['PARTYID'] in request_data['user_id']]

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
