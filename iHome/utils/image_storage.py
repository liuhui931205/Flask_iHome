# coding=utf-8
import qiniu

access_key = 'uzc59bVURbUbazey9vrexXKocNKBUN8NuLijk57N'
secret_key = '-9lenw28jU2REojvGkcsEPWk5Nm9V2HIVqb5Nkts'

bucket_name = 'ihome26'


def image_storage(data):
    q = qiniu.Auth(access_key, secret_key)
    token = q.upload_token(bucket_name)
    ret, info = qiniu.put_data(token, None, data)

    if info.status_code == 200:
        key = ret.get('key')
        return key
    else:
        raise Exception('上传文件失败')
