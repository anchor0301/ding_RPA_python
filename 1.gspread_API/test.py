import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]
json_file_name = 'puppyhome-ab3080785244.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1npWlDUeHFClI2An3MYrCTJipUX3dXJpRemZUKL31BAw/edit#gid=0'
# 스프레스시트 문서 가져오기
doc = gc.open_by_url(spreadsheet_url)
# 시트 선택하기
worksheet = doc.worksheet('시트1')


#특정 셀 데이터 가져오기
cell_data = worksheet.acell("d8").value

start_date = worksheet.acell("g8").value
end_date = worksheet.acell("h8").value
day =int(start_date)-int(end_date)

예약_완료=cell_data+"님 예약이 완료 되었습니다."
print(day)
print(예약_완료)

#행 데이터 가져오기
column_data = worksheet.row_values(2)
print(column_data)