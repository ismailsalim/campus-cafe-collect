from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from main.lambdautils.BaseLambdaHandler import BaseLambdaHandler
from math import cos, pi
from decimal import Decimal
import json


class GetVenuesHandler(BaseLambdaHandler):
    """
    handler to return all venues in the database
    """

    def __init__(self, dbObject):
        super().__init__(dbObject)

    def handle_request(self, event: dict, context: dict) -> dict:
        table = self.db.getTable()

        queryList = event['query'].lower().split()
        minPrice = event['pricemin']
        maxPrice = event['pricemax']
        longitude = float(event['longitude'])
        latitude = float(event['latitude'])
        radius = float(event['radius'])
        minLong, maxLong, minLat, maxLat = self.convertKmToDegrees(longitude, latitude, radius)

        requestedRestaurant = json.loads(event['restaurants'].lower())
        requestedBar = json.loads(event['bars'].lower())
        requestedCafe = json.loads(event['cafes'].lower())
        requestedTypes = self.getTypes(requestedRestaurant, requestedBar, requestedCafe)

        try:
            response = table.scan()
        except ClientError as e:
            return {
                'statusCode': self.clientErrorCode
            }

        venues = response['Items']
        returnVenuesList = []
        for venue in venues:
            if venue['typeid'] not in requestedTypes:
                continue
            tags = venue['tags']
            name = venue['name']
            venueID = venue['venueid']
            typeID = venue['typeid']

            if self.queryMatched(queryList, name.lower(), tags):
                result = table.scan(
                    FilterExpression=(
                            Attr("venueid").eq(venueID) &
                            Attr("typeid").eq(typeID) &
                            Attr("pricerank").between(str(minPrice), str(maxPrice)) &
                            Attr("longitude").between(Decimal(str(minLong)), Decimal(str(maxLong))) &
                            Attr("latitude").between(Decimal(str(minLat)), Decimal(str(maxLat)))
                    ))
                item = result['Items']
                if item:
                    returnVenuesList.append(item[0])
        if returnVenuesList:
            return {
                'statusCode': 200,
                'body': returnVenuesList
            }
        else:
            return {
                'statusCode': 201,
                'body': returnVenuesList
            }

    def queryMatched(self, queries: list, name: str, tags: list) -> bool:
        return self.tagMatched(queries, tags) or self.nameMatched(queries, name)

    @staticmethod
    def tagMatched(queries: list, tags: list) -> bool:
        for tag in tags:
            for query in queries:
                if query in tag:
                    return True
        return False

    @staticmethod
    def nameMatched(queries: list, name: str) -> bool:
        if not queries:
            return True
        for query in queries:
            if query in name:
                return True
        return False

    @staticmethod
    def getTypes(isRestaurant: bool, isBar: bool, isCafe: bool) -> list:
        # returns a list of types requested by user
        # if type is not specified, the default is all venues
        types = []
        if isRestaurant:
            types.append("1")
        if isBar:
            types.append("2")
        if isCafe:
            types.append("3")
        if len(types) == 0:
            return ["1", "2", "3"]
        return types

    @staticmethod
    def convertKmToDegrees(longitude: float, latitude: float, radiusInKm: float) -> tuple:
        kmInLongitudeDegree = 111.320 * cos(latitude / 180.0 * pi)
        deltaLong = radiusInKm / kmInLongitudeDegree
        deltaLat = radiusInKm / 111.1

        min_lat = latitude - deltaLat
        max_lat = latitude + deltaLat
        min_long = longitude - deltaLong
        max_long = longitude + deltaLong

        return min_long, max_long, min_lat, max_lat
