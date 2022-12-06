# Pianote
### 피아노 GUI로 간단하게 작곡하는 프로그램  
**Note** : 음표 (2분음표, 4분음표, 8분음표, 16분음표)  
**Pitch** : 음 (C D E F G A B, 도레미파솔라시)

<br/>

## 사용 라이브러리

### Pygame 2.1.2
+ 라이선스 정보 : [LGPL License](https://www.pygame.org/docs/LGPL.txt)

<br/>

## 기능설명

### 피아노 조작
1. 키보드 키로 피아노 조작 가능(음표 작성)  
오른손 키 레이아웃 : **w 3 e 4 r 5 t**  /  **y 7 u 8 i**  /  **o 0 p - [ = ]**  
왼손 키 레이아웃 : **z s x d c**  /  **v g b h n j m**
1. 좌우방향키(←→)로 오른손 키 레이아웃의 옥타브 이동가능
1. 상하방향키(↑↓)로 왼손 키 레이아웃의 옥타브 이동가능
1. 마우스로 피아노 건반 클릭시 소리 출력은 가능(단, 음표가 입력되지는 않음)
1. **ESC** 키를 누르면 프로그램이 종료되고 지금까지 입력된 악보 저장
1. **ENTER** 키를 누르면 지금까지 작성한 악보 재생  

### 음표 조작
1. 음표 좌클릭시 클릭한 음표 다음부터 입력커서 이동
1. 음표 우클릭시 클릭한 음표 삭제
1. **DELETE** 키를 누르면 가장 마지막에 쓰인 음표 삭제
1. 특정 음표위에서 마우스 휠업하면 음이 길어짐(ex : 4분음표 → 2분음표)
1. 특정 음표위에서 마우스 휠다운하면 음이 짧아짐(ex : 4분음표 → 8분음표)

<br/>

## 참고자료

### 피아노 GUI 디자인 및 기능 설정 참고
+ plemaster01의 PythonPiano : [Git link](https://github.com/plemaster01/PythonPiano/blob/main/main.py)  

### 원본 음원 파일 정보
[University of IOWA : Electronic Music Studios](https://theremin.music.uiowa.edu/MISpiano.html)  
+ Please consider making a tax-deductible donation to fund the next phase of this project. Beginning in 2012, instruments are being recorded at 24/96 with three mics for mono and stereo files that are archived into Zip files. For online listening, these notes are also organized into 16/44.1 chromatic scale files. Each instrument in the collection will be re-recorded with a variety of articulations, legato, glissandi, multiphonics, extended techniques, and in combination with other instruments. New instruments, such as the recently added guitar, will also be recorded. These freely available recordings have been used by countless musicians and in over 270 research papers. When making a donation, please write "Electronic Music Studios" in the comments field.
+ Instrument :	Piano  
+ Model :	Steinway & Sons model B
+ Performer :	Evan Mazunik
+ Date :		November 5 & 27, 2001
+ Location :	2017 Voxman Music Building
+ Technician :	Michael Cash
+ Distance :	Left mic 8" above center bass strings, Right mic 8" above center treble strings
+ Microphone :	Neumann KM 84
+ Mixer :		Mackie 1402-VLZ
+ Recorder :	Panasonic SV-3800 DAT
+ Format :	16-bit, 44.1 kHz, stereo
+ Comments : stereo, non-anechoic recording  
<br/>
위 무료 음원을 .wav로 변환,  
음원을 trim하여 음 시작점을 맞추는 작업을 하고  
포맷에 맞게 파일명을 수정해서 사용하였음.
