import jwt


# 生成JWT Token
def generate_token(payload, secret_key, algorithm='HS256'):
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


# 验证JWT Token
def verify_token(token, secret_key, algorithms=None):
    if algorithms is None:
        algorithms = ['HS256']
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithms)
        return payload
    except jwt.ExpiredSignatureError:
        # Token过期
        return None
    except jwt.InvalidTokenError:
        # 无效的Token
        return None


# 示例用法
if __name__ == '__main__':
    # 定义payload
    payload = {
        'user_id': 123,
        'username': 'example_user'
    }

    # 定义密钥
    secret_key = '666'

    # 生成JWT Token
    token = generate_token(payload, secret_key)
    print('JWT Token:', token)

    # 验证JWT Token
    verified_payload = verify_token(token, secret_key)
    if verified_payload:
        print('Verified Payload:', verified_payload)
    else:
        print('Token verification failed')
