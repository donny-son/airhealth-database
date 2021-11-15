### Vehicle Registration

Therefore, a newer approach is required via the [Molit OpenAPI Service](https://stat.molit.go.kr/portal/api/main.do).

0. Create `molit` openapi account. https://stat.molit.go.kr/portal/auth/memberJoin1.do

1. Request service key. https://stat.molit.go.kr/portal/api/auth/apply.do
   Note that the service key is immediately generated upon registration.

   1. 사용목적 및 활용용도: 미세먼지 대기오염 예측 모델 구축 연구 활용

   2. 서비스 URL: https://www.ncc-gcsp.ac.kr:8443/n_academics/kimsunyoung.jsp

   3. 설명: 미세먼지 대기오염 예측 모델 구축을 위해서는 교통망, 지역별 차량등록대수, 항만 위치 데이터 등 다양한 요인들과 코호트 환자의 거리를 측정한 지리변수들이 필요하기 때문에 이에 따라 신청함.

2. Request OpenAPI access. https://stat.molit.go.kr/portal/api/open/list.do

3. `사용가능한 오픈API > 교통/물류 > 자동차등록현황보고 > 자동차등록대수현황_시도별 (1990 - 2021)`

   1. 오픈API 사용목적: 미세먼지 대기오염 예측 모델 구축을 위해서는 지역별 자동차등록대수 현황과 코호트 환자의 거리를 측정한 지리변수들이 필요하기 때문에 이에 따라 신청함.
   2. `중복된 목록...` 이슈 발생함. 그러나 이는 사실 불필요한 과정임. API endpoint URL에 사전에 본인이 발급받은 인증키를 사용하면 내려받기가 가능함

4. Test with `wget`.

   ```sh
   wget  http://stat.molit.go.kr/portal/openapi/service/rest/getList.do\?key\=인증키\&form_id\=5559\&style_num\=1\&start_dt\=201303\&end_dt\=201303
   ```

