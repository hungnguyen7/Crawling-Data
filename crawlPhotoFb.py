import os, re, requests
print('Đăng nhập vào facebook, nhấn F12, chọn Tab Storage\nChọn Cookies bên trái màn hình\nLưu ý đến 2 value cua c_user và xs')
cUser=input('Nhập value của c_user: ')
print('Lưu ý chỉ lấy value xs từ đầu đến hết dấu % thứ 5')
print('Mẫu xs hợp lệ: https://miro.medium.com/max/875/1*bDk2Bu3wavwgzlGkZKhLxg.png')
xs=input('Nhập value của xs: ')
cookies = {
    "c_user": cUser,
    "xs": xs
}
print('Copy đường dẫn facebook cá nhân của người bạn muốn lấy ảnh\nTruy cập vào link: https://lookup-id.com \nPaste đường dẫn vừa copy và nhấn Lookup\nFacebook Id hợp lệ sẽ có dạng: 100005580631191')
friend_id = input("Nhập friend id(phải là số): ")
folderName=input('Nhập tên thư mục bạn muốn lưu ảnh: ')
# load anh tu link
def load_photo(input_url):
    req=requests.Session()
    offset=0 # so thu tu album anh la boi so cua 12
    while True:
        # Url de download anh
        url='{}{}'.format(input_url, offset)
        # Yeu cau ket noi bang cookies cua nguoi su dung
        res=req.get(url, cookies=cookies)
        # Noi dung html tra ve chuyen sang dang text
        html=res.text
        #re.findall se tra ve danh sach cac link hinh anh co trong content
        # Link co dang nhu sau
        #<a href="/photo.php?fbid=RANDOM_NUMBER&amp;...&amp;source=56" class="ba bb bc">
        # Ta ca tim gia tri fbid=RANDOM_NUMBER do
        match = re.findall(r"/photo.php\?fbid=([0-9]*)&amp;", html)
        if match:
            for imageLink in match:
                # Tao ten file anh, chuan bi ghi du lieu
                f=open('{}/{}.jpg'.format(folderName, imageLink), 'wb')
                # Lay duong dan toi hinh, tra ve source html
                res = req.get("https://mbasic.facebook.com/photo/view_full_size/?fbid={}".format(imageLink), cookies=cookies)
                imageText=res.text
                # Tim duong dan goc den file hinh anh
                searchImageFile=re.search(r"a href=\"(.*?)\"", imageText)
                if searchImageFile:
                    # URL duong dan den hinh anh goc
                    url=str(searchImageFile.groups()[0]).replace("&amp;", "&")
                    # Lay anh ve
                    res=req.get(url, cookies=cookies)
                    # Ghi anh vao bo nho
                    f.write(res.content)
                    f.close()
                else:
                    break
            offset+=12
        else:
            print('Download Completed')
            break
#Tao thu muc co ten folder name
if __name__ == "__main__":
    if not os.path.exists(folderName):
        os.makedirs(folderName)
url_photo_tag = "https://mbasic.facebook.com/{}/photoset/pb.{}.-2207520000../?owner_id={}&offset=".format(friend_id, friend_id, friend_id)
#link album fb se co dang https://mbasic.facebook.com/FB-ID/photoset/t.FB_ID/?owner_id=FB_ID&offset=(gia tri off la so va boi so cua 12)
url_photo_upload = "https://mbasic.facebook.com/{}/photoset/t.{}/?owner_id={}&offset=".format(friend_id, friend_id, friend_id)
load_photo(url_photo_tag)
load_photo(url_photo_upload)