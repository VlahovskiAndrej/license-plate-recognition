import cv2
import numpy as np
import imutils
import easyocr

img = cv2.imread('sample_images/car_3.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("image_normal", img)
cv2.waitKey(0)

cv2.imshow("image_gray", cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
cv2.waitKey(0)

bfilter = cv2.bilateralFilter(gray, 11, 17, 17)

cv2.imshow("noise_reduction_bilateral_filter", cv2.cvtColor(bfilter, cv2.COLOR_BGR2RGB))
cv2.waitKey(0)

edged = cv2.Canny(bfilter, 30, 200)

cv2.imshow("edge_recognition_canny", cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
cv2.waitKey(0)

keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:100]

location = None
for contour in contours:
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.018 * peri, True)
    if len(approx) == 4:
        location = approx
        break

mask = np.zeros(gray.shape, np.uint8)
cv2.drawContours(mask, [location], 0, 255, -1)
new_image = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("with_mask", cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
cv2.waitKey(0)

(x, y) = np.where(mask == 255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

cv2.imshow("only_reg_plate", cropped_image)

reader = easyocr.Reader(['en'])
result = reader.readtext(cropped_image)

with open('registration_plates_output.txt', 'a') as file:
    print("Added to plate_recognition.txt: ")
    for (_, text, _) in result:

        cleaned_text = ""
        for char in text:
            if char.isdigit() or char.isspace() or char.isupper():
                cleaned_text += char
            else:
                cleaned_text += ' '
        text = cleaned_text
        text = text.replace('\n+', ' ')

        file.write(f'{text} ')
        print(f'{text}', end=" ")
    file.write(f'\n')

cv2.waitKey(0)