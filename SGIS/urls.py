"""
https://sgis.kostat.go.kr/developer/html/openApi/api/data.html#51

ADM : 행정
    ADM_CD : 행정구역 코드
    ADM_BORDER : 행정구역 경계

"""
URLS = {
        "AUTH": "https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json",
        "STAGE": "https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json",
        "HADMAREA": "https://sgisapi.kostat.go.kr/OpenAPI3/boundary/hadmarea.geojson",
        "GEOCODING": "https://sgisapi.kostat.go.kr/OpenAPI3/addr/geocode.json"
        }
