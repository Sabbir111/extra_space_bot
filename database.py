from mongoengine import *
import datetime
import os



#DB_URI = "mongodb+srv://test:test@cluster0.nqwsp.mongodb.net/newdb?authSource=admin&replicaSet=atlas-93t93s-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true"
DB_URI = os.environ.get("Database_string")
connect(host=DB_URI)
print(DB_URI)
try:
    class Records(Document):
        owner = ObjectIdField(required=True)
        size = StringField(required=True)
        climateControl = BooleanField(default=False, required=True)
        price = FloatField(required=True)
        date = DateTimeField(default=datetime.datetime.utcnow)


    def push_records(_id, size, climate_control, price, ):

        all_records = Records(owner=_id,
                              size=size,
                              climateControl=climate_control,
                              price=price

                              )

        all_records.save()


    # push_records("10 x 10",False,100,)
    # push_records("60fff17fd2936c16d4039681","10 x 10",False,10.20)

    class Links(Document):
        link = StringField(required=True)
        websiteName = StringField()
        location = StringField()
        createdAt = DateTimeField(default=datetime.datetime.utcnow)


    def push_links(link, website_name):

        all_links = Links(link=link,
                          websiteName=website_name
                          )

        all_links.save()
    # push_links("https://www.extraspace.com/storage/facilities/us/colorado/colorado_spring/",
    #            "www.extraspace.com")

except Exception as e:
    print(e)
