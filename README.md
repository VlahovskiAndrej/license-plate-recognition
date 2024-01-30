# Детекција на регистарски таблички и препознавање на карактери

**Опис**
- Во документацијата за овој проект ќе ги разгледа основните компоненти на оваа апликација
за детекција на регистарски таблички во детали, почнувајќи од земањето и
предпроцесирањето на слики, потоа ке ги разгледаме намалувањето на шумот, детекцијата
на рабовите, анализата на контурите и техниките за препознавање на знаци, откривајќи го
сложениот механизам на работење на секој чекор.<br/>

**Користени библиотеки** <br/><br/>
  ![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/e8528a38-d252-42d0-baec-a3dfd1dbc330)

**Вчитување на слика**
- Најпрво вчитуваме една слика во случајов “car_5.png” преку функцијата
cv2.imread(). Потоа мора да ја направиме сликата црно-бела бидејки сите слики се многу
полесни така за било какви обработки и манипулации. Тоа го правиме со методот
cv2.cvtColor() и одбираме cv2.COLOR_BGR2GRAY, односно да се направи промена на
пикселите од BGR (Blue, Green, Red) во GRAY, односно црно-бели.<br/><br/>
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/aec5f64a-6393-4854-b63c-b62c58777fed)

**Намалување на шумот**
- Ке ја користиме техниката на Bilateral Filtering
(Билатерално филтрирање). Ова е пософистицирана техника за намалување на шумот која
ги задржува рабовите додека ги замаглува областите со слични бои. Таа ја зема во предвид
и близината и сличноста на боите кога го пресметува просекот за секој пиксел. Ова е
многу корисно кога е важно да се задржат деталите на сликата.
Билатерално филтрирање користиме преку функцијата cv2.bilateralFilter() од
библиотеката OpenCV. <br/><br/>
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/8cee94f9-c607-4194-85ec-948ab7a8b186)
<br/><br/>
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/efca5548-b0bd-474d-9d47-4d097a897b55)

**Наогање на рабови**
- Во оваа ситуација најдобро одговара Canny Edge Detector. Тој е познат по
отпорнаста на шум, со што се откриваат само значајните рабови. Работи на принцип на
прво изгладнување (Smoothing), после бара нагли промени во градиентот на боите, се
отргнуваат слабите рабови и за крај со “Hysteresis” се поврзуваат пикселите на рабовите со
предвидување. Ова прави непрекинати рабови и ги елеминира изолираните пиксели.<br/><br/>
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/08c28eba-80a3-4e61-a445-05c1098463f7)
<br/><br/>
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/894e8562-daff-48fe-a715-98c09f5b1dc0)

**Барање на правоаголник**
- Следен чекор за најдеме таблицата е да најдеме перфектен четириаголник на
сликата. Тоа ке направиме со неколку чекори. Најпрво треба да ги најдеме контурите во
сликата со функцијата cv2.findContours(). Ова ни врака листа од сите контури пронајдени
на сликата според “keypoints”. <br/><br/>
  ![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/f27a97f6-34ad-41ba-8fde-b734dc4ac442)
  ![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/e90cfee6-03a1-495d-b0a4-e6dfdc0d24cb)
  ![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/df686703-c83f-493c-a83b-f748feb6d915)
  
- За од овие “keypoints” да ги добиеме вистинските контурни линии ја користиме
функцијата од imutils: imutils.grab_contours(keypoints)
- После ова за да го олесниме процесот на избирање правоаголник ке ги одбереме
100те најголеми контури. Ова го правиме со методот sorted()
- Следно треба да ја најдеме најголемата форма која има 4 рабови.
  ![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/0d45eaa1-f92b-468b-b5a0-821fe7c25b48)
  ![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/db225065-30b9-4464-a53a-03ef0275c5c8)

**Креирање на маска**
- Најпрово иницијализираме црна маска со истите димензии како сликата.
Функцијата np.zeros() од NumPy се користи за да се создаде низа исполнета со нули.
Податочниот тип е специфициран како np.uint8, што значи дека секој пиксел во маската
може да има вредности во опсегот [0, 255]. Почетно, сите пиксели во маската се поставени
на 0, односно се црни.<br/><br/>
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/6f328abc-b26b-4677-bfdf-23073b33855d)

- После ова треба контурата дефинирана со променливата location (која претставува
четириаголник) да се нацрта врз маската. Функцијата cv2.drawContours() го прави тоа со
примање на неколку аргументи:
0: Индексот на контурата во листата. Во овој случај, има само една контура во листата, па
нејзиниот индекс е 0.
255: Вредноста на бојата која сакате да се користи за цртање на контурата. Тука е
поставена на 255, што одговара на бела боја.
-1: Овој параметар специфицира дека сакате да го исполните контурата со одредената боја.
Практично, целата област затворена со контурата станува бела на маската.<br/><br/>
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/95c5ad7a-345f-45d1-b697-957fa0eb94ed)
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/c4165274-e3d2-43cb-91c2-e5fa7f9439c1)

- Следно извршуваме операција на битово И (Bitwise AND) помеѓу оригиналната
слика (img) и маската (mask) користејќи ја функцијата cv2.bitwise_and().
Резултатот од оваа операција е нова слика каде само регионот специфициран со
маската е видлив, а останатата слика е црна. Практично, ja изолира областа од сликата која
одговара на детектираната контура.<br/><br/>
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/97c163ba-8f91-4f4e-a7c8-a733030311e2)
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/f74f53f3-325d-4b64-ae11-63939184b385)

- И за крај го отсрануваме црниот дел од сликата и ни останува само регистрацијата
на посебна слика. Тоа го правиме со следниот код.<br/><br/>
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/5f449d0a-003e-4707-a93d-66b199397401)
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/5396897a-c7ba-452b-8c6a-38f00907fb36)

**Optical Character Recognition (OCR)**
- OCR софтверот ги лоцира регионите во сликата каде што се наоѓа текстот. Тој ги
идентификува границите на поединечни знаци, зборови и пасуси и ги анализира облиците
обидувајки се да ги препознае. Тоа се прави со база на познати знаци. Напредни OCR
системи користат алгоритми за машинско учење, како невронски мрежи, за да го подобрат
квалитетот на распознавањето
- Првично иницијализираме OCR читач користејќи го EasyOCR. Создаваме инстанца
на класата Reader и наведувате дека треба да се распознае текст на англиски (['en']). Ова
значи дека OCR машината ќе се обиде да распознае и извлече текст на англиски јазик од
сликата.<br/><br/>
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/fe54e8c4-aebe-474b-8a7c-bdc5b04753bc)
- Следно сликата која што содржи текст, се предава на OCR читачот (reader). Се
повикува методот readtext() на класата Reader за да се обработи сликата и да се извлече
секој текст што може да се пронајде.
Резултатот се зачувува во променливата result. Овој резултат обично содржи листа
на региони со текст заедно со соодветниот распознат текст и координати на рамки околу
текстот.<br/><br/>
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/bcec966e-17e2-4e37-8b94-fb0ba4dbb47e)

- Понатаму овој резултат треба да го зачуваме во .тхт документ односно во
“registration_plates.txt”. Toa го правиме со отворање на текстуална датотека наречена
'registration_plates.txt' во режим на 'допишување' ('append') и запишуваме текстуални
податоци во неа, базирани на result (резултатот) што го добиеме од операцијата за оптичко
распознавање на знаци (OCR).<br/><br/>
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/a3971cbf-deff-4ef6-9a3c-d6e29a071f91)
![image](https://github.com/VlahovskiAndrej/license-plate-recognition/assets/95543841/a473ec6b-2bcb-456f-8552-656df3f6edd1)
