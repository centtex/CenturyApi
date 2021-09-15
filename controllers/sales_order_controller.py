from flask import jsonify, request, Response
from sqlalchemy.sql import text
from caching import CacheData
from firebase_wrap import FirebaseAuthenticate
from dateutil import parser
from models import db
from common.helper import Helper


class SalesOrder:

    def __init__(self):
        self.cache = CacheData()
        self.helper = Helper()

    def getSalesOrderDetails(self, user_id):
        if request.method == 'POST':
            if FirebaseAuthenticate.get_user_token(user_id):
                request_data = request.get_json()
                if 'cmp_code' in request_data and 'user_id' in request_data and \
                        'order_id' in request_data and 'from_date' in request_data \
                        and 'to_date' in request_data and 'agent_id' in request_data \
                        and 'pagenumber' in request_data and 'pagesize' in request_data:

                    cached_data = self.cache.get_data('sales_order' + '-data')

                    if cached_data is None:
                        sql_stmt = "SELECT O.*, Price_Name FROM(" \
                                   "SELECT SO.AGENT_ID,SO.LGR_ID AS PARTYID,SO.CMP_CODE,SO.ORDER_TYPE,SO.FLAG" \
                                   ",SO.SAL_ORDER_ID,SO.CONFNO,SO.SALES_ORDERNO,SO.THROUGH,SO.VCH_DATE" \
                                   ",SO.ORDER_DATE,SO.START_DATE,SO.END_DATE,SO.Scheme,SO.SCHEME_PER,SO.Price_id" \
                                   ",LM.LGR_NAME AS PARTY,PCM.CITY_NAME AS PARTY_CITY, PCM.CITY_DISTRICT" \
                                   ",UPPER(LM.LGR_NAME) AS PARTYNAME,UPPER(LM.LGR_ADD1) AS LGR_ADD1" \
                                   ",UPPER(LM.LGR_ADD2) AS LGR_ADD2,UPPER(LM.LGR_ADD3)AS LGR_ADD3" \
                                   ",LM.CITY_PINCODE,ALM.LGR_NAME AS AGENT,ACM.CITY_NAME AS AGENT_CITY" \
                                   ",TM.TRANSPORT_NAME,IM.ITEM_NAME,SOD.BALES,SOD.RATE,SOD.RATEDIFF" \
                                   ",SOD.REMARK, SOD.Item_ID,SM.SCREEN_NAME,SCM.CITY_NAME AS STATION " \
                                   "FROM salesorder SO INNER JOIN  salesorderdetail SOD " \
                                   "ON SO.SAL_ORDER_ID=SOD.SAL_ORDER_ID AND SO.CMP_CODE=SOD.CMP_CODE " \
                                   "LEFT JOIN  ledgermaster LM ON LM.LGR_ID = SO.LGR_ID " \
                                   "LEFT JOIN  citymaster PCM ON LM.CITY_ID=PCM.CITY_ID " \
                                   "LEFT JOIN  ledgermaster ALM ON ALM.LGR_ID=SO.AGENT_ID " \
                                   "LEFT JOIN  citymaster ACM ON ACM.CITY_ID=ALM.CITY_ID " \
                                   "LEFT JOIN  transportmaster TM ON TM.TRANSPORT_ID=SO.TRANSPORT_ID " \
                                   "LEFT JOIN  itemmaster IM ON SOD.ITEM_ID=IM.ITEM_ID " \
                                   "LEFT JOIN  screenmaster SM ON SM.SCREEN_ID=SOD.SCREEN_ID " \
                                   "LEFT JOIN citymaster SCM ON SCM.CITY_ID=SO.STATION_ID) O " \
                                   "INNER JOIN pricelist PL ON PL.Price_ID=O.Price_id and PL.Item_Id = O.Item_ID " \
                                   "WHERE O.CMP_CODE = %(cmpcode)s AND O.ORDER_TYPE='B' AND O.FLAG='S'" \
                                   "" % {"cmpcode": request_data['cmp_code']}
                        sql_stmt += " ORDER BY O.VCH_DATE DESC"
                        sales_data = db.session.execute(text(sql_stmt), {"db": "classicmodels"})
                        cached_data = [sales._asdict() for sales in sales_data.all()]
                        self.cache.set_data('sales_order' + '-data', cached_data)

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

                    if request_data['order_id']:
                        cached_data = [d for d in cached_data if d['SALES_ORDERNO'] == request_data['order_id']]

                    if request_data['from_date']:
                        from_date = parser.parse(request_data['from_date'])
                        cached_data = list(filter(lambda x: x['VCH_DATE'] >= from_date, cached_data))

                    if request_data['to_date']:
                        to_date = parser.parse(request_data['to_date'])
                        cached_data = list(filter(lambda x: x['VCH_DATE'] <= to_date, cached_data))

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
