**qwen2.5-coder:1.5b + Ollama + Continue 설정 방법**

Radeon 780M(공유 메모리) 환경에 잘 맞는 가벼운 조합입니다.  
주로 **자동완성(Autocomplete)**용으로 최적화되어 있고, Chat도 같이 쓸 수 있습니다.

### 1. Ollama 모델 다운로드

터미널(또는 명령 프롬프트)에서 아래 명령어를 실행하세요.

```bash
# Ollama가 실행 중인지 확인
ollama serve

# 모델 다운로드 (약 1GB)
ollama pull qwen2.5-coder:1.5b
```

(선택) 자동완성에 더 좋은 base 버전을 원하면:
```bash
ollama pull qwen2.5-coder:1.5b-base
```

다운로드 확인:
```bash
ollama list
```

### 2. Continue 설정 파일 열기

1. VS Code에서 Continue 사이드바 열기
2. 하단 톱니바퀴 아이콘 클릭 → **Open Config**  
   또는  
   `Ctrl + Shift + P` → **Continue: Open Config File**

파일 위치:
- Windows: `%USERPROFILE%\.continue\config.yaml`
- macOS/Linux: `~/.continue/config.yaml`

### 3. 추천 설정 (config.yaml)

아래 내용을 **전체 교체**하거나 기존 내용에 맞춰 수정하세요.

#### 가장 추천 (1.5b를 자동완성 전용 + Chat에도 사용)

```yaml
name: Local Qwen 1.5B
version: 0.0.1
schema: v1

models:
  - name: Qwen2.5-Coder 1.5B
    provider: ollama
    model: qwen2.5-coder:1.5b
    apiBase: http://localhost:11434
    roles:
      - chat
      - edit
      - apply
      - autocomplete

  - name: Nomic Embed
    provider: ollama
    model: nomic-embed-text
    apiBase: http://localhost:11434
    roles:
      - embed
```

#### 자동완성만 1.5b로 쓰고 싶을 때 (Chat은 나중에 다른 모델로 바꿀 수 있음)

```yaml
name: Local Qwen Autocomplete
version: 0.0.1
schema: v1

models:
  - name: Qwen2.5-Coder 1.5B (Autocomplete)
    provider: ollama
    model: qwen2.5-coder:1.5b
    apiBase: http://localhost:11434
    roles:
      - autocomplete

  # Chat용으로 나중에 7b나 3b를 추가할 수 있음
  # - name: Qwen2.5-Coder 7B
  #   provider: ollama
  #   model: qwen2.5-coder:7b
  #   apiBase: http://localhost:11434
  #   roles:
  #     - chat
  #     - edit
  #     - apply
```

저장 후 VS Code를 한 번 재시작하거나 Continue에서 **Reload Config**를 눌러주세요.

### 4. 테스트 방법

1. 아무 코드 파일 열기
2. 코드를 입력하다가 멈추면 회색 글씨로 자동완성 제안이 나오는지 확인
3. `Tab` 키로 수락
4. Continue 채팅 창에서 질문해보기

### 추가 팁 (Radeon 780M 최적화)

- 자동완성이 느리면 `debounceDelay`를 늘려보세요 (아래처럼 추가 가능):
  ```yaml
  autocompleteOptions:
    debounceDelay: 300
    maxPromptTokens: 1024
  ```
- Embeddings도 쓰고 싶으면 추가로:
  ```bash
  ollama pull nomic-embed-text
  ```

설정 후 문제가 생기면 `ollama list` 결과나 config.yaml 내용을 알려주세요. 바로 수정해 드리겠습니다!