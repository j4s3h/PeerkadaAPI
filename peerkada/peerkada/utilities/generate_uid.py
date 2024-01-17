import shortuuid

def generate_uuid(length=5):
    uid = shortuuid.ShortUUID().random(length=length)
    return uid
