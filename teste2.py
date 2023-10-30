from robot.gen3.connect_gen3 import ConnectGen3
from robot.gen3.move_gen3 import MoveGen3
import easyocr
import time
import pyrealsense2 as rs
import numpy as np
import cv2
from itertools import combinations_with_replacement

#TODO: teste utilizando variações no threshold no canny e usando uma lista de posições

def extreme_points(reference_sum, points_auxiliary, list_sum):  # Define os pontos 1 e 4 de uma área com 4 pontos

    if reference_sum == list_sum[0]:
        order_point = [points_auxiliary[0, 0, 0], points_auxiliary[0, 0, 1]]
        sum_number = 0

    elif reference_sum == list_sum[1]:
        order_point = [points_auxiliary[1, 0, 0], points_auxiliary[1, 0, 1]]
        sum_number = 1

    elif reference_sum == list_sum[2]:
        order_point = [points_auxiliary[2, 0, 0], points_auxiliary[2, 0, 1]]
        sum_number = 2

    elif reference_sum == list_sum[3]:
        order_point = [points_auxiliary[3, 0, 0], points_auxiliary[3, 0, 1]]
        sum_number = 3

    return order_point, sum_number


def sum_to_zero(sum_number, list_sum):  # Usado para resetar as somas para zero

    if sum_number == 0:
        list_sum[0] = 0

    if sum_number == 1:
        list_sum[1] = 0

    if sum_number == 2:
        list_sum[2] = 0

    if sum_number == 3:
        list_sum[3] = 0
    return list_sum


def organize_points(image_dilate):

    list_areas = []
    list_points = []
    list_points_intern = []
    area_auxiliary = 0
    points_auxiliary = 0
    contours, hierarchy = cv2.findContours(image_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for element_contours in contours:
        area = cv2.contourArea(element_contours)
        list_areas.append(area)
        perimeter = cv2.arcLength(element_contours, True)
        approx = cv2.approxPolyDP(element_contours, 0.02 * perimeter, True)
        list_points.append(approx)

    points_auxiliary_counter = 0

    for element_areas in list_areas:

        if element_areas > area_auxiliary:  # Search the biggest area
            area_auxiliary = element_areas

            if len(list_points[points_auxiliary_counter]) == 4:  # Verify if have an area with four points
                points_auxiliary = list_points[points_auxiliary_counter]

        points_auxiliary_counter = points_auxiliary_counter + 1

    sum0 = points_auxiliary[0, 0, 0] + points_auxiliary[0, 0, 1]
    sum1 = points_auxiliary[1, 0, 0] + points_auxiliary[1, 0, 1]
    sum2 = points_auxiliary[2, 0, 0] + points_auxiliary[2, 0, 1]
    sum3 = points_auxiliary[3, 0, 0] + points_auxiliary[3, 0, 1]

    list_sum = [sum0, sum1, sum2, sum3]
    biggest_sum = max(list_sum)
    smallest_sum = min(list_sum)

    # Determine the order of the points
    point4, sum_number = extreme_points(biggest_sum, points_auxiliary, list_sum)
    list_sum_with_zero = sum_to_zero(sum_number, list_sum)
    point1, sum_number = extreme_points(smallest_sum, points_auxiliary, list_sum)
    list_sum_with_zero = sum_to_zero(sum_number, list_sum_with_zero)

    points_auxiliary_counter = 0
    for element_areas in list_sum_with_zero:

        if element_areas != 0:
            list_points_auxiliary = [points_auxiliary[points_auxiliary_counter, 0, 0],
                                     points_auxiliary[points_auxiliary_counter, 0, 1]]
            list_points_intern.append(list_points_auxiliary)
        points_auxiliary_counter += 1

    if list_points_intern[0][0] > list_points_intern[1][0]:
        point2 = list_points_intern[0]
        point3 = list_points_intern[1]

    else:
        point3 = list_points_intern[0]
        point2 = list_points_intern[1]

    list_out_points = [point1[0], point1[1], point2[0], point2[1], point3[0], point3[1], point4[0], point4[1]]

    return list_out_points

#Função utilizada para obter as combinações de thresholds
def list_thresholds():

    list_1 = [10, 20, 30, 40, 50, 60]
    list_2 = [60, 50, 40, 30, 20, 10]
    combination_1= combinations_with_replacement(list_1, 2)
    combination_2 = combinations_with_replacement(list_2, 2)
    combination = list(combination_1) + list(combination_2)
    combination_no_duplicates = list(dict.fromkeys(combination))

    return combination_no_duplicates


def rectify(frame):

    try:  # No caso de não haver um frame de saida na função, retorna o frame de entrada

        image_blur = cv2.GaussianBlur(frame, (7, 7), 1)
        image_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
        image_canny = cv2.Canny(image_gray, 30, 20, 3)
        kernel = np.ones((5, 5))
        image_dilate = cv2.dilate(image_canny, kernel, iterations=1)
        list_out_points = organize_points(image_dilate)
        matrix_points_in = np.float32(
            [[list_out_points[0], list_out_points[1]], [list_out_points[2], list_out_points[3]],
             [list_out_points[4], list_out_points[5]], [list_out_points[6], list_out_points[7]]])
        matrix_points_out = np.float32([[0, 0], [1280, 0], [0, 720], [1280, 720]])
        matrix = cv2.getPerspectiveTransform(matrix_points_in, matrix_points_out)
        rectify = cv2.warpPerspective(frame, matrix, (1280, 720))

        return rectify

    except Exception as e:
        print('Error:', e)


        return frame


def apply_EasyOCR(image):

    reader = easyocr.Reader(['pt', 'en'])
    result = reader.readtext(image, detail=0, allowlist='1234567890')

    return result


def image_processing(frame):

    frame_resize = cv2.resize(frame, (1300, 300))
    frame_gray = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2GRAY)
    frame_blur = cv2.medianBlur(frame_gray, 5)
    frame_adptive = cv2.adaptiveThreshold(frame_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 3)
    frame_bilateral = cv2.bilateralFilter(frame_adptive, 20, 200, 250)

    return frame_bilateral


def avaliation(frame):

    # frame_rectify = rectify(frame)
    image_processed = image_processing(frame)
    ocr_result = apply_EasyOCR(image_processed)

    return ocr_result


# TODO: testar mais tratamentos de imagem--
# TODO: testar o rastreamento com a função e depois treinar o yolo pra testar com ele.
# TODO: Verificar a possibilidade de fazer a ánelise cega com a repartição das unidades da tela
img = cv2.imread('C:/Users/jsff/Desktop/TCC/Gen3/telaP1.jpg')
a = avaliation(img)
print(a)