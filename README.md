# intel_L515_playground

just for fun

# 협업자에게.

- 본 리포지토리는 본래 인텔 라이다센서(L515)의 읽기 및 확장 개발을 위한 "SDK"를 이해하고, 사용해보기 위한 목적으로 만들어 졌으나, 현재는 그 명목을 이어, 범용 라이다센서를 구축하기 위해 필요한 소프트웨어적 자원들을 모아두고 공유하는 목적으로 논문에 참조될 것을 염두에 두고 유지되고 있음을 알림.

## git과 github가 익숙하지 않은 자들을 위한 설명서

- 좋은 개발자라면, 자신의 파일을 깃으로 관리하고, 깃허브에 올려, 원격 서버에서 관리되고, 공유될 수 있도록 유지해야만 합니다.
- 리포지토리 동기화
  - 코드파일들은 종종 여러 컴퓨터에서 동시에 작업되곤 합니다.(특히 지금처럼, 작업자가 여러명일 경우, 작업하는 내용이 충돌될 수 있겠죠?)
  - 따라서, 아래의 지침에 따라 작업을 진행해주서야만 합니다.
    1. vscode 좌측 사이드 바 위에서 세번째의 git모양 버튼 (소스 제어)을 누릅니다.
    - 원한다면 github desktop을 이용해도 무관합니다(github desktop은 바탕화면에 있습니다.)
    2. 새로고침을 누릅니다.
    - github desktop에는 Fetch origin이라고 써져있습니다.
    3. 만약 Pull 해야 할 커밋이 있다면, 하세요.
    4. 작업을 진행합니다.
    5. 중간중간 저장해야 할 때마다, 습관적으로 저장하고, 커밋을 작성하세요(제목이 없으면 안됩니다. 대충 지어도 무관합니다.)
    6. 퇴근할때, upstream에 푸쉬합니다.
    7. 할 수 있다면, origin에 patch하세요.

## 웹캠을 이용하여 2d 센싱을 하는 방법

#### 파일 설명

- 웹캠 관련 파일들은 모두 [opencv_practice](opencv_practice) 폴더에 있습니다.
- [cam.py](opencv_practice/cam.py)
  - 캠을 불러오고, 초기화하고, 영상을 송출하도록 하는 코드입니다.
  - 코드의 10번 줄을 봐주세요. <br>
    `a = cv.VideoCapture(1)`
    <br>
    코드에 원인 모를 문제가 생겼다면, 여기의 숫자를 먼저 0으로 바꿔주세요.
  - 실행 후, 작은 화면 하나가 생겼다면, 정상입니다.
  - 해당 화면을 클릭한 후, 키보드의 c를 누르면, 캡쳐됩니다!
    - 터미널에 캡처 소요시간과, 타임스탬프가 찍히니 참고해주세요.
  - <strong>해당 화면을 끄고싶다면, q를 누르세요</strong>. x버튼 눌러도 안닫힙니다.
  - 캡쳐된 파일들은 [captured](captured)로 갑니다.
- [captured](captured)
  - 캡쳐된 파일들의 보관함입니다.
- [function_tool.py](opencv_practice/function_tool.py)
  - 기타 잡다한 필요한 함수들을 여기에 선언해뒀습니다.
  - 거리측정 식도 여기에 있습니다.
  - (TODO) 높이포함 거리측정식도 추가될 예정입니다.
  - 아마 직접 건들 일은 없을겁니다...
- [image_processing.py](opencv_practice/image_processing.py)
  - 아무것도 아닙니다.
  - opencv 연습한다고 만들어뒀던겁니다.
- [pre_process_redchannal_threshold.py](opencv_practice/pre_process_redchannal_threshold.py)
  - 아마 여기만 죽도록 만질겁니다.
  - 10번 줄의 `FILE_PATH` 위치에 있는 파일을 불러와, 잡다한 이미지 처리를 진행합니다.
    - 오류가 있다면, 재일 먼저, `FILE_PATH`를 잘 설정했는지 확인해주세요.
    - 원하는 파일의 절대 위치를 쌍따옴표로 감싸주어야 합니다.
  - 현재 세팅은, 마스크 영역과, 찾은 dot 영역의 활성화를 보여줄 겁니다.
  - 실행을 하시고, 터미널을 보시면, 각 함수별 실행 시간과, 찾은 dot의 위치, dot 영역의 크기(반지름)을 현시해줍니다.

---

### you can download Intel RealSence SDK 2.0 below the link

https://github.com/IntelRealSense/librealsense/releases/tag/v2.54.2

---

### here is the Intel RealSence SDK Wiki

https://github.com/IntelRealSense/librealsense/wiki

---

### let's get sample file from here

https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python/examples

### list of package which is need to pre-load

- pip install opencv-python
  - it will be cv2
- pip install pyrealsense2
- pip install numpy
