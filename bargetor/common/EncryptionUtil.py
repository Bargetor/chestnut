def md5(string):
    md5 = hashlib.md5()
    md5.update(string)
    md5_str = md5.hexdigest()
    return md5_str

def sha(string):
    sha1= hashlib.sha1()
    sha1.update(splice_str)
    sha1_str = sha1.hexdigest()
    return sha1_str
