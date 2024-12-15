from config import db

class itemInfo(db.Model):
    itemName = db.Column(db.String(100), unique = False, nullable = False)
    itemScore = db.Column(db.Integer, primary_key = True)

    def to_json(self):
        return {
            "itemName": self.itemName,
            "itemScore": self.itemScore
        }