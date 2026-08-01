**Sourcetree에서 다른 컴퓨터에 SSH 키 생성하는 방법**

다른 컴퓨터에서 새로 SSH 키를 만들고 Sourcetree에 설정하는 방법입니다.  
(Windows 기준으로 가장 많이 쓰는 방법 위주로 설명합니다.)

### 1. Sourcetree에서 SSH 키 생성 (가장 쉬운 방법)

1. **Sourcetree**를 실행합니다.
2. 상단 메뉴에서 **도구(Tools) → SSH 키 생성/가져오기(Create or Import SSH Keys)** 를 선택합니다.
3. **PuTTY Key Generator** 창이 뜹니다.
4. **Generate** 버튼을 클릭합니다.
5. 창 안에서 마우스를 마구 움직여 키를 생성합니다. (진행 바가 다 찰 때까지)
6. 키가 생성되면:
   - **Key passphrase** / **Confirm passphrase**에 비밀번호를 입력합니다. (선택 사항이지만 권장)
   - **Save public key** → `.pub` 파일로 저장 (예: `id_rsa.pub`)
   - **Save private key** → `.ppk` 파일로 저장 (예: `id_rsa.ppk`)
7. 저장 위치는 보통 `C:\Users\사용자이름\.ssh` 폴더를 추천합니다.

### 2. 공개키를 Git 서비스에 등록

생성된 **공개키(.pub)** 내용을 복사해서 등록해야 합니다.

- **GitHub**: Settings → SSH and GPG keys → New SSH key
- **Bitbucket**: Personal settings → SSH keys → Add key
- **GitLab**: Preferences → SSH Keys

공개키 내용 확인 방법:
- 메모장으로 `.pub` 파일을 열어서 전체 내용을 복사하거나
- PuTTY Key Generator 창에 보이는 공개키 부분을 복사

### 3. Sourcetree에 비밀키 등록

**방법 A. Pageant 사용 (PuTTY 방식)**
1. 시스템 트레이(작업표시줄 오른쪽)에서 **Pageant** 아이콘을 찾습니다. (모자 쓴 컴퓨터 아이콘)
2. 없으면 Sourcetree에서 **도구 → Pageant 시작**을 실행합니다.
3. Pageant 아이콘을 우클릭 → **Add Key**
4. 방금 저장한 `.ppk` 파일을 선택하고 비밀번호를 입력합니다.

**방법 B. OpenSSH 방식 사용**
1. Sourcetree → **도구 → 옵션(Options)** → **일반(General)** 탭
2. **SSH 클라이언트**를 **OpenSSH**로 변경
3. SSH 키 경로에 개인키 파일(`id_rsa` 또는 생성한 파일)을 지정

### 4. 추가 팁 (다른 컴퓨터에서 기존 키를 쓰고 싶을 때)

- **기존 키를 복사**하는 경우:
  - 이전 컴퓨터의 `.ppk` 또는 `id_rsa` / `id_rsa.pub` 파일을 USB나 클라우드로 새 컴퓨터로 옮깁니다.
  - 새 컴퓨터의 `.ssh` 폴더에 넣고 위 3번 방법으로 등록하면 됩니다.
- **OpenSSH로 새로 생성**하고 싶을 때 (터미널 사용):
  ```bash
  ssh-keygen -t ed25519 -C "your_email@example.com"
  ```
  또는
  ```bash
  ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
  ```

### 확인 방법

터미널(또는 Sourcetree 터미널)에서 아래 명령어로 테스트해보세요.

```bash
ssh -T git@github.com
```
(또는 bitbucket.org / gitlab.com)

성공하면 “Hi username! You’ve successfully authenticated...” 같은 메시지가 나옵니다.

---

**주의사항**
- 비밀키(`.ppk` 또는 `id_rsa`)는 **절대** 공유하거나 공개하지 마세요.
- 새 컴퓨터마다 키를 새로 만드는 것을 추천합니다. (보안상 더 안전)

원하시는 방식이 **Windows**인지 **Mac**인지, 또는 **기존 키 복사**인지 **새로 생성**인지 알려주시면 더 정확하게 안내해 드릴게요!



**Python 설치 + pip 설정 방법**

Python을 설치하면 **pip**도 기본적으로 함께 설치됩니다.  
가장 추천하는 방법을 알려드릴게요.

### 1. Python 공식 사이트에서 설치 (Windows 추천)

1. [Python 공식 다운로드 페이지](https://www.python.org/downloads/)에 접속합니다.
2. **Download Python 3.x.x** 버튼을 클릭해서 최신 버전을 받습니다.
3. 다운로드한 설치 파일을 실행합니다.
4. **중요!**  
   설치 화면 맨 아래에서  
   ✅ **Add python.exe to PATH**  
   이 체크박스를 **반드시 체크**합니다.
5. **Install Now**를 눌러 설치를 진행합니다.

### 2. 설치 확인

설치가 끝나면 **명령 프롬프트(cmd)** 또는 **PowerShell**을 새로 열고 아래 명령어를 입력하세요.

```bash
python --version
```

```bash
pip --version
```

정상적으로 설치됐다면 버전 정보가 나옵니다.  
(예: `Python 3.13.x`, `pip 25.x.x`)

### 3. pip가 없다고 나올 때 (수동 설치)

드물게 pip가 빠진 경우가 있습니다. 아래 명령어로 설치하세요.

```bash
python -m ensurepip --upgrade
```

또는

```bash
python -m pip install --upgrade pip
```

그래도 안 되면:

1. [get-pip.py](https://bootstrap.pypa.io/get-pip.py) 파일을 다운로드
2. 다운로드한 폴더에서 명령어 실행:
   ```bash
   python get-pip.py
   ```

### 4. 자주 쓰는 명령어

| 목적              | 명령어                          |
|-------------------|---------------------------------|
| 패키지 설치       | `pip install 패키지이름`        |
| 패키지 업그레이드 | `pip install --upgrade 패키지이름` |
| 설치된 패키지 확인| `pip list`                      |
| pip 자체 업그레이드| `python -m pip install --upgrade pip` |

---

**팁**
- Windows에서 `python` 대신 `py` 명령어도 많이 사용합니다.
- 가상환경(venv)을 쓰면 프로젝트별로 패키지를 분리할 수 있어서 더 좋습니다.
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

Mac이나 Linux에서 설치하는 방법도 필요하시면 말씀해주세요!