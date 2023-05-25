# -*- coding: utf-8 -*-
import json
import pygame
import time, sys


def gamepad(queue):
    pygame.init()
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("No gamepad found.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Gamepad Name:", joystick.get_name())
    print("Number of Buttons:", joystick.get_numbuttons())
    print("Number of Axes:", joystick.get_numaxes())

    # 创建一个窗口
    # window_width = 640
    # window_height = 480
    # window = pygame.display.set_mode((window_width, window_height))
    # buffer_surface = pygame.Surface((window_width, window_height))
    # pygame.display.set_caption("Gamepad")

    # def printText(str, text_color, x=0, y=0):
    #     font = pygame.font.Font(None, 28)
    #     font.set_bold(False)
    #     text_color = (255, 255, 255)
    #     text = font.render(str, True, text_color)
    #     buffer_surface.blit(text, (x, y))

    # def printLines(text_lines):
    #     font_file = "src/font/msyh.ttc"
    #     font = pygame.font.Font(font_file, 14)
    #     font.set_bold(False)
    #     text_color = (255, 255, 255)
    #     y = 10
    #     for line in text_lines:
    #         text = font.render(line, True, text_color)
    #         buffer_surface.blit(text, (10, y))
    #         y += 24

    # def clearWindow():
    #     buffer_surface.fill((0, 0, 0))

    running = True

    clock = pygame.time.Clock()

    #fps
    fps = 60
    # 按钮
    btn = -1

    # 摇杆移动的阈值
    movement_threshold = 0.2

    # 扳机 左
    left_tigger_id = -1
    left_tigger_moving = False
    left_tigger_value = -1

    # 扳机 右
    right_tigger_id = -1
    right_tigger_moving = False
    right_tigger_value = -1

    # 摇杆 左 x
    left_axis_x_id = -1
    left_axis_x_moving = False
    left_axis_x = 0

    # 摇杆 左 y
    left_axis_y_id = -1
    left_axis_y_moving = False
    left_axis_y = 0

    # 摇杆 右 x
    right_axis_x_id = -1
    right_axis_x_moving = False
    right_axis_x = 0

    # 摇杆 右 y
    right_axis_y_id = -1
    right_axis_y_moving = False
    right_axis_y = 0

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            # 清空 buffer_surface
            # buffer_surface.fill((0, 0, 0))
            # 获取手柄按钮状态
            if event.type == pygame.JOYBUTTONDOWN:
                press = True
                btn = event.button
            elif event.type == pygame.JOYBUTTONUP:
                # 按钮操作

                # 退出程序
                # if btn == 5:
                #     pygame.quit()
                #     sys.exit()

                press = False
                btn = -1

            elif event.type == pygame.JOYAXISMOTION:
                # 检查摇杆是否移动

                if event.axis == 0:
                    if abs(event.value) > movement_threshold:
                        left_axis_x_id = event.axis
                        left_axis_x_moving = True
                        left_axis_x = event.value
                    elif abs(event.value) <= movement_threshold:
                        left_axis_x_moving = False
                        left_axis_x = 0

                elif event.axis == 1:
                    if abs(event.value) > movement_threshold:
                        left_axis_y_id = event.axis
                        left_axis_y_moving = True
                        left_axis_y = event.value
                    elif abs(event.value) <= movement_threshold:
                        left_axis_y_moving = False
                        left_axis_y = 0
                elif event.axis == 2:
                    if abs(event.value) > movement_threshold:
                        right_axis_x_id = event.axis
                        right_axis_x_moving = True
                        right_axis_x = event.value
                    elif abs(event.value) <= movement_threshold:
                        right_axis_x_moving = False
                        right_axis_x = 0
                elif event.axis == 3:
                    if abs(event.value) > movement_threshold:
                        right_axis_y_id = event.axis
                        right_axis_y_moving = True
                        right_axis_y = event.value
                    elif abs(event.value) <= movement_threshold:
                        right_axis_y_moving = False
                        right_axis_y = 0
                elif event.axis == 4:
                    if event.value > 0:
                        left_tigger_id = event.axis
                        left_tigger_moving = True
                        left_tigger_value = event.value
                    elif event.value <= 0:
                        left_tigger_moving = False
                        left_tigger_value = -1
                elif event.axis == 5:
                    if event.value > 0:
                        right_tigger_id = event.axis
                        right_tigger_moving = True
                        right_tigger_value = event.value
                        joystick.rumble(1, 1, 100)
                    elif event.value <= 0:
                        right_tigger_moving = False
                        right_tigger_value = -1

            # if press == True:
            #     printText("Button Pressed: " + str(btn), text_color);

            # if tigger == True:
            #     printText("Tigger: " + str(tigger_id) + ":" + str(tigger_value), text_color, 0, 100);

            # if joystick_moving == True:
            #     printText("Axis: " + str(axis_id) + ":" + str(axis_value), text_color, 0, 200);

            # text_lines = [
            #     "fps: " + str(clock.get_fps()),
            #     "btn: " + str(btn),
            #     "left_tigger_value: " + str(left_tigger_value),
            #     "right_tigger_value: " + str(right_tigger_value),
            #     "left_axis_x: " + str(left_axis_x),
            #     "left_axis_y: " + str(left_axis_y),
            #     "right_axis_x: " + str(right_axis_x),
            #     "right_axis_y: " + str(right_axis_y),
            # ]

            json_data = {
                # "fps": clock.get_fps(),
                "power_level": joystick.get_power_level(),
                "btn": btn,
                "left_tigger_value": left_tigger_value,
                "right_tigger_value": right_tigger_value,
                "left_axis_x": left_axis_x,
                "left_axis_y": left_axis_y,
                "right_axis_x": right_axis_x,
                "right_axis_y": right_axis_y,
            }

            queue.put(json.dumps(json_data).encode('utf-8'))

            # printLines(text_lines)
            # window.blit(buffer_surface, (0, 0))
            # pygame.display.flip()
