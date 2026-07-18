✅ 최종 완전판 Markdown 파일 (Git 설치 방법까지 상세히 추가)

아래 내용을 그대로 복사해서 setup-guide.md 파일로 저장하세요.

MySQL + Git 완전 설치 및 설정 가이드 (2026년 최신)

작성일: 2026년 7월  
대상: 개발 완전 초보자  
목적: 무료 DBMS 추천부터 MySQL, Git 설치 및 프로젝트 관리까지 한 번에 정리

목차
무료 DBMS 추천
MySQL 설치 (Windows)
Git 설치 (.exe 파일)
Git 최초 설정
프로젝트 Git 등록 및 GitHub 연동
기본 Git 명령어 모음
.gitignore 예시
팁 및 문제 해결

1. 무료 DBMS 추천

| DBMS          | 유형          | 추천 상황                          | 특징 |
|---------------|---------------|------------------------------------|------|
| SQLite    | 파일 기반     | 개인 프로젝트, 모바일, 테스트     | 설치 없이 바로 사용 가능 |
| PostgreSQL| 관계형        | 웹/모바일 백엔드, 복잡한 쿼리     | 가장 강력하고 표준 준수 |
| MySQL     | 관계형        | 웹사이트, PHP, 일반 웹 개발       | 가장 대중적 |
| MariaDB   | 관계형        | MySQL 대체                         | 더 자유로운 오픈소스 |
| MongoDB   | NoSQL         | 유연한 데이터 구조, 현대 앱       | JSON 형태 |

초보자 추천 순서: SQLite → MySQL → PostgreSQL

2. MySQL 설치 (Windows)

2.1 다운로드
MySQL Installer 다운로드 페이지
MySQL Installer for Windows (64-bit) 선택 후 다운로드

2.2 설치 단계
.msi 파일 실행
Setup Type → Developer Default (추천)
제품 선택
   MySQL Server 8.0
   MySQL Workbench (강력 추천)
Root Password 설정 (꼭 기억!)
Windows Service로 등록 (자동 시작)
설치 완료 후 Workbench로 연결 테스트

2.3 확인 명령어
mysql -u root -p

3. Git 설치 (.exe 파일)

3.1 다운로드
공식 사이트: https://git-scm.com/download/win
Git-2.x.x-64-bit.exe** 파일이 자동으로 다운로드됩니다.

3.2 설치 마법사 상세 설정 (중요!)
라이선스 동의 → Next
설치 위치 → 기본값 그대로 Next
Select Components → 기본 체크 유지
Start Menu Folder → Next
Choosing the default editor → Use Visual Studio Code 추천
Adjusting your PATH environment  
   → Git from the command line and also from 3rd-party tools (가장 중요!)
HTTPS transport → OpenSSL 선택
Line ending conversion → Checkout Windows-style, commit Unix-style 추천
Terminal emulator → Use MinTTY (Git Bash 예쁘게)
기타 옵션 → 기본값으로 Install

3.3 설치 완료 후 확인
Git Bash 또는 명령 프롬프트에서 실행:
git --version
→ git version 2.x.x.windows.1 나오면 성공!

4. Git 최초 설정 (한 번만 실행)

git config --global user.name "너의이름"
git config --global user.email "your-email@example.com"

설정 확인
git config --global --list

5. 프로젝트 Git 등록 및 GitHub 연동

5.1 로컬 초기화
cd 프로젝트_폴더
git init
git add .
git commit -m "첫 커밋: MySQL 프로젝트 초기 설정"

5.2 GitHub 연동
GitHub에서 새 Repository 생성
터미널에서 실행:
git remote add origin https://github.com/너의아이디/레포이름.git

https://github.com/pandaru99/PythonTest.git
git branch -M main
git push -u origin main

6. 기본 Git 명령어 모음

| 명령어                        | 설명 |
|-------------------------------|------|
| git status                  | 현재 상태 |
| git add .                   | 모든 파일 등록 |
| git commit -m "메시지"      | 커밋 |
| git push                    | 업로드 |
| git pull                    | 내려받기 |
| git log --oneline           | 커밋 로그 |
| git clone [URL]             | 저장소 복제 |

7. .gitignore 예시

데이터베이스
*.sql
*.bak
*.dump

환경파일
.env
.env.local

의존성
node_modules/
pycache/

IDE
.vscode/
.idea/

OS
.DS_Store
Thumbs.db

8. 팁 및 문제 해결

Git 명령어가 안 먹힐 때** → PC 재부팅 또는 PATH 수동 추가
MySQL 비밀번호 초기화** → MySQL Installer 실행
GitHub 푸시 인증 오류** → Personal Access Token 생성 또는 Git Credential Manager 사용
추천 조합**: VS Code + Git 내장 + MySQL Workbench
Mac 사용자** → brew install mysql / brew install git
Linux (Ubuntu)** → sudo apt install mysql-server git

이 파일 하나로 MySQL + Git 완벽 세팅 가능합니다!

필요하면 Linux/Mac 버전 전체 추가, MySQL Workbench 상세 사용법, Git 브랜치 전략 등 더 확장해드릴게요.  
파일 저장 후 자유롭게 사용하세요! 🚀

이 버전이 가장 빠짐없이 정리된 최종판입니다.  
복사해서 바로 .md 파일로 만들어 사용하시면 됩니다!  
추가 수정 원하는 부분 있나요?