import json
import requests
from .models import User, Day, Cool, Attendance, Menu
from django.db.models import Count
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime

LINE_CHANNEL_ACCESS_TOKEN = settings.LINE_CHANNEL_ACCESS_TOKEN

# ◯✕カレンダーを生成する関数
def generate_flex_message(cool_number, user_id):
    # クールに紐づく日付を取得
    cool = Cool.objects.get(number=cool_number)
    days = Day.objects.filter(cool=cool).order_by('date')

    # 5日ずつのグループに分ける
    grouped_days = [days[i:i + 5] for i in range(0, len(days), 5)]

    # Flex Messageの構造を作成（クール名を保持）
    flex_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{cool_number}クール",
                            "weight": "bold",
                            "size": "xl",
                            "gravity": "center"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "他クール",
                                "text": "お休み登録"
                            }
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "月", "align": "center"},
                        {"type": "text", "text": "火", "align": "center"},
                        {"type": "text", "text": "水", "align": "center"},
                        {"type": "text", "text": "木", "align": "center"},
                        {"type": "text", "text": "金", "align": "center"}
                    ]
                }
            ]
        }
    }

    # ユーザーの出欠情報を取得
    user = User.objects.get(line_id=user_id)
    attendances = {att.day_id: att.is_present for att in Attendance.objects.filter(user=user, day__in=days)}

    # 各日のボタンを作成
    for row in grouped_days:
        # 日付のテキストを追加
        flex_message["body"]["contents"].append({
            "type": "box",
            "layout": "horizontal",
            "contents": [{"type": "text", "text": day.date.strftime("%-m/%-d"), "align": "center"} for day in row]
        })

        # ボタンの行を作成
        button_row = []
        for day in row:
            if day.id not in attendances:
                default_is_present = not day.is_holiday  # 休業日ならFalse, 営業日ならTrue
                Attendance.objects.create(user=user, day=day, is_present=default_is_present)
                attendances[day.id] = default_is_present  # デフォルトを設定
            if day.is_holiday:
                
                button_row.append({
                    "type": "text",
                    "text": "休",
                    "align": "center",
                    "gravity": "center"
                })
                
            else:
                is_present = attendances.get(day.id, True)  # 出欠情報がない場合はデフォルトで「◯」
                label = "◯" if is_present else "✕"
            
                button_row.append({
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": label,
                        "data": f"{str(cool_number)}:{str(day.date)}"
                    }
                })

        # Flex Message にボタンの行を追加
        flex_message["body"]["contents"].append({
            "type": "box",
            "layout": "horizontal",
            "contents": button_row
        })
        
    flex_message["body"]["contents"].append({
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "button",
                "action": {
                "type": "postback",
                "label": "全部✕",
                "data": f"{str(cool_number)}:none"
                }
            },
            {
                "type": "button",
                "action": {
                "type": "postback",
                "label": "全部◯",
                "data": f"{str(cool_number)}:all"
                }
            }
        ]
    })

    return flex_message    

# 注文数カレンダーを生成する関数
def generate_calender(cool_number):
    # クールに紐づく日付を取得
    cool = Cool.objects.get(number=cool_number)
    days = Day.objects.filter(cool=cool).order_by('date')

    # 5日ずつのグループに分ける
    grouped_days = [days[i:i + 5] for i in range(0, len(days), 5)]

    # Flex Messageの構造を作成（クール名を保持）
    flex_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{cool_number}クール注文数",
                            "weight": "bold",
                            "size": "xl",
                            "gravity": "center"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "他クール",
                                "text": "全員の予定"
                            }
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "月", "align": "center", "gravity": "center"},
                        {"type": "text", "text": "火", "align": "center", "gravity": "center"},
                        {"type": "text", "text": "水", "align": "center", "gravity": "center"},
                        {"type": "text", "text": "木", "align": "center", "gravity": "center"},
                        {"type": "text", "text": "金", "align": "center", "gravity": "center"}
                    ]
                }
            ]
        }
    }

    # 各日のボタンを作成
    for row in grouped_days:
        # 日付のテキストを追加
        flex_message["body"]["contents"].append({
            "type": "box",
            "layout": "horizontal",
            "contents": [{"type": "text", "text": day.date.strftime("%-m/%-d"), "align": "center", "gravity": "center"} for day in row]
        })

        # ボタンの行を作成
        button_row = []
        for day in row:
            if day.is_holiday:
                button_row.append({
                    "type": "text",
                    "text": "休",
                    "align": "center",
                    "gravity": "center"
                })
                
            else:
                delivery_count = Attendance.objects.filter(day__date=day.date, is_present=True).count()
                button_row.append({
                    "type": "text",
                    "text": str(delivery_count),
                    "align": "center",
                    "gravity": "center"
                })

        # Flex Message にボタンの行を追加
        flex_message["body"]["contents"].append({
            "type": "box",
            "layout": "horizontal",
            "contents": button_row,
            "paddingTop": "sm",
            "paddingBottom": "sm"
        })
        
    return flex_message

# Flex Message (お休み登録クール選択)
cool_select_no = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "クール選択",
                "weight": "bold",
                "size": "xl"
            }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "3クール",
                    "data": "休3クール"
                }
            },
            {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "5クール",
                    "data": "休5クール"
                }
            }
        ]
    }
}
# Flex Message (支払いクール選択)
cool_select_pay = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "クール選択",
                "weight": "bold",
                "size": "xl"
            }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "3クール",
                    "data": "払3クール"
                }
            },
            {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "5クール",
                    "data": "払5クール"
                }
            }
        ]
    }
}
# Flex Message (全員のカレンダークール選択)
cool_select_cal = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "クール選択",
                "weight": "bold",
                "size": "xl"
            }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "3クール",
                    "data": "全3クール"
                }
            },
            {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "5クール",
                    "data": "全5クール"
                }
            }
        ]
    }
}
# Flex Message (全員の金額クール選択)
cool_select_sum = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "クール選択",
                "weight": "bold",
                "size": "xl"
            }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "3クール",
                    "data": "金3クール"
                }
            },
            {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "5クール",
                    "data": "金5クール"
                }
            }
        ]
    }
}
# Flex Message (献立表選択)
menu_select = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "text",
            "text": "何月？",
            "weight": "bold",
            "size": "xl",
            "gravity": "center"
          },
          {
            "type": "button",
            "action": {
                "type": "message",
                "label": "戻る",
                "text": "電話献立"
            }
          }
        ]
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
                "type": "postback",
                "label": "1月",
                "data": "献立&1月"
            }
          },
          {
            "type": "button",
            "action": {
                "type": "postback",
                "label": "2月",
                "data": "献立&2月"
            }
          }
        ]
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
                "type": "postback",
                "label": "4月",
                "data": "献立&4月"
            }
          },
          {
            "type": "button",
            "action": {
                "type": "postback",
                "label": "5月",
                "data": "献立&5月"
            }
          }
        ]
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
                "type": "postback",
                "label": "6月",
                "data": "献立&6月"
            }
          },
          {
            "type": "button",
            "action": {
                "type": "postback",
                "label": "7月",
                "data": "献立&7月"
            }
          }
        ]
      }
    ]
  }
}
# Flex Message (電話・献立メニュー)
tel_select = {
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "電話・献立表",
        "size": "xl",
        "weight": "bold"
      }
    ]
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "お店に電話",
          "text": "電話"
        }
      },
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "献立表を見る",
          "data": "献立"
        }
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "今日のお弁当の数",
          "text": "今日のお弁当の数"
        }
      },
    ]
  }
}
# Flex Message (電話) 
tel_message = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "url",
    "size": "full",
    "aspectRatio": "20:10",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "https://line.me/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "weight": "bold",
        "size": "lg",
        "text": "店名"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "住所",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "住所",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "text",
            "text": "営業時間",
            "color": "#aaaaaa",
            "size": "sm"
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "月",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1,
                "align": "center"
              },
              {
                "type": "text",
                "text": "12:00 - 14:30",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "火 - 日",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1,
                "align": "center"
              },
              {
                "type": "text",
                "text": "12:00 - 14:30, 18:00 - 21:00",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "電話",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1,
                "align": "center"
              },
              {
                "type": "text",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "text": "0120-000-000"
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "CALL",
          "uri": "tel:0120-000-000"
        }
      }
    ],
    "flex": 0
  }
}

# LINEのWebhookを受け取る
@csrf_exempt
def line_webhook(request):
    body = json.loads(request.body.decode("utf-8"))
    
    for event in body.get("events", []):
        reply_token = event["replyToken"]
        user_id = event["source"]["userId"]
        start_loading_animation(user_id)
        # ユーザーが初めて登録した場合
        if event["type"] == "follow":
            # ニックネームを尋ねるメッセージを送信（リプライ）
            reply_message(reply_token, "こんにちは！まずはお名前を教えてください。")

        # Postback イベントの処理
        elif event["type"] == "postback":
            postback_data = event["postback"]["data"]
            
            # お休み管理の方
            if ":" in postback_data:

                # 日付情報を取得（例: "2025-04-01" のような形式）
                cool_number, day_date = postback_data.split(":")
                
                #全部◯
                if day_date == "all":
                    # ユーザーを取得（まだ登録されていない場合は新規作成）
                    user, created = User.objects.get_or_create(line_id=user_id)

                    # クール番号に基づいてそのユーザーのすべての出欠情報を取得
                    try:
                        # 該当するクールのすべての日付で出欠情報を更新
                        cool = Cool.objects.get(number=int(cool_number))
                        days_in_cool = Day.objects.filter(cool=cool)  # cool_numberでフィルタリング

                        # 出欠情報をすべて「出席」状態に変更
                        for day in days_in_cool:
                            attendance, created = Attendance.objects.get_or_create(user=user, day=day)
                            if day.is_holiday:                            
                                attendance.is_present = False
                                attendance.save()
                            else:
                                attendance.is_present = True
                                attendance.save()                            

                        text_message = "すべての日を◯に変更"
                        flex_message = generate_flex_message(int(cool_number), user_id)
                        reply_two_message(reply_token, "休みの日を選択", text_message, flex_message)

                    except Day.DoesNotExist:
                        reply_message(reply_token, "指定されたクールの日付が存在しません。")

                #全部✕
                elif day_date == "none":
                    # ユーザーを取得（まだ登録されていない場合は新規作成）
                    user, created = User.objects.get_or_create(line_id=user_id)

                    # クール番号に基づいてそのユーザーのすべての出欠情報を取得
                    try:
                        # 該当するクールのすべての日付で出欠情報を更新
                        cool = Cool.objects.get(number=int(cool_number))
                        days_in_cool = Day.objects.filter(cool=cool)  # cool_numberでフィルタリング

                        # 出欠情報をすべて「不在」状態に変更
                        for day in days_in_cool:
                            attendance, created = Attendance.objects.get_or_create(user=user, day=day)
                            if day.is_holiday:                            
                                attendance.is_present = False
                                attendance.save()
                            else:
                                attendance.is_present = False
                                attendance.save()       

                        text_message = "すべての日を✕に変更"
                        flex_message = generate_flex_message(int(cool_number), user_id)
                        reply_two_message(reply_token, "休みの日を選択", text_message, flex_message)

                    except Day.DoesNotExist:
                        reply_message(reply_token, "指定されたクールの日付が存在しません。")
                
                #クール番号:日付
                else:
                    # ユーザーを取得（まだ登録されていない場合は新規作成）
                    user, created = User.objects.get_or_create(line_id=user_id)
                    
                    try:
                        # 対応する日付の取得
                        day = Day.objects.get(date=day_date)
                        
                        # 出欠情報を取得または作成
                        attendance, created = Attendance.objects.get_or_create(user=user, day=day)

                        # 出欠情報を切り替え
                        attendance.is_present = not attendance.is_present
                        attendance.save()

                        # 結果をユーザーに返信
                        day_date = datetime.strptime(day_date, "%Y-%m-%d").date()
                        formatted_date = day_date.strftime("%m/%d")
                        text_message = f"{formatted_date}を{'◯に変更' if attendance.is_present else '✕に変更'}"
                        flex_message = generate_flex_message(int(cool_number), user_id)
                        reply_two_message(reply_token, "休みの日を選択", text_message, flex_message)

                    except Day.DoesNotExist:
                        reply_message(reply_token, "指定された日付が存在しません。")
            
            # 献立・電話の方
            elif "&" in postback_data:
                kondate, month = postback_data.split("&")
                
                try:
                    # 月に対応する number を取得
                    month_to_number = {
                        "1月": 1, "2月": 2, "4月": 4, "5月": 5, "6月": 6, "7月": 7
                    }
                    
                    if month in month_to_number:
                        menu = Menu.objects.get(number=month_to_number[month])
                        # 画像URLを取得し、完全なURLを生成
                        if not menu.menu_image:
                            reply_message(reply_token, f"{month}の献立画像が設定されていません。")
                            return

                        # `settings.BASE_URL` を使って完全なURLにする
                        menu_image_url = f"{settings.BASE_URL}{menu.menu_image.url}"
                        reply_image_message(reply_token, f"{month}献立表", menu_image_url, menu_image_url)
                    else:
                        reply_message(reply_token, f"{month}の献立表は未登録です。")

                except Menu.DoesNotExist:
                    reply_message(reply_token, f"{month}の献立表は未登録です。")
            
            # その他メッセージ
            else:
                match postback_data:
                    case "休3クール":
                        cool_id = 3
                        flex_message = generate_flex_message(cool_id, user_id)
                        reply_flex_message(reply_token, "休みの日を選択", flex_message)
                    
                    case "休5クール":
                        cool_id = 5
                        flex_message = generate_flex_message(cool_id, user_id)
                        reply_flex_message(reply_token, "休みの日を選択", flex_message)
                    
                    case "払3クール":
                        try:                    
                            # そのクールに関連する出欠情報を取得し、出席している日の数をカウント
                            attendance_count = Attendance.objects.filter(user__line_id=user_id, day__cool__number=3, is_present=True).count()

                            # 金額を計算（出席日数 * 250）
                            total_amount = attendance_count * 250

                            # 結果をユーザーに返信
                            reply_message(reply_token, f"3クール: {attendance_count}個、金額: {total_amount:,}円")

                        except Day.DoesNotExist:
                            reply_message(reply_token, "指定されたクールの日付が存在しません。")
                    
                    case "払5クール":
                        try:                    
                            # そのクールに関連する出欠情報を取得し、出席している日の数をカウント
                            attendance_count = Attendance.objects.filter(user__line_id=user_id, day__cool__number=5, is_present=True).count()

                            # 金額を計算（出席日数 * 250）
                            total_amount = attendance_count * 250

                            # 結果をユーザーに返信
                            reply_message(reply_token, f"5クール: {attendance_count}個、金額: {total_amount:,}円")

                        except Day.DoesNotExist:
                            reply_message(reply_token, "指定されたクールの日付が存在しません。")
                    
                    case "全3クール":
                        flex_message = generate_calender(3)
                        reply_flex_message(reply_token, "3クールの全員の予定", flex_message)

                    case "全5クール":
                        flex_message = generate_calender(5)
                        reply_flex_message(reply_token, "5クールの全員の予定", flex_message)
                    
                    case "金3クール":
                        # すべてのユーザーの出席数を取得
                        attendance_summary = (
                            Attendance.objects.filter(day__cool__number=3, is_present=True)
                            .values('user__name')  # ユーザー名でグループ化
                            .annotate(attendance_count=Count('id'))  # 出席数をカウント
                        )

                        # メッセージを作成
                        summary_text = "\n".join(
                            [f"{entry['user__name']}: {entry['attendance_count']}個、金額: {entry['attendance_count'] * 250:,}円" for entry in attendance_summary]
                        )

                        # 返信メッセージを送信
                        reply_message(reply_token, f"3クール全員の金額:\n{summary_text}")
                    
                    case "金5クール":
                        # すべてのユーザーの出席数を取得
                        attendance_summary = (
                            Attendance.objects.filter(day__cool__number=5, is_present=True)
                            .values('user__name')  # ユーザー名でグループ化
                            .annotate(attendance_count=Count('id'))  # 出席数をカウント
                        )

                        # メッセージを作成
                        summary_text = "\n".join(
                            [f"{entry['user__name']}: {entry['attendance_count']}個、金額: {entry['attendance_count'] * 250:,}円" for entry in attendance_summary]
                        )

                        # 返信メッセージを送信
                        reply_message(reply_token, f"5クール全員の金額:\n{summary_text}")
                    
                    case "献立":
                        reply_flex_message(reply_token, "クールを選択", menu_select)
                    
                    case _:
                        reply_message(reply_token, "不正なpostback")

        # ユーザーがメッセージを送信した場合
        elif event["type"] == "message" and event["message"]["type"] == "text":
            message = event["message"]["text"]
            
            match message:
                case "お休み登録":
                    reply_flex_message(reply_token, "クールを選択", cool_select_no)
                    
                case "支払金額":
                    reply_flex_message(reply_token, "クールを選択", cool_select_pay)
                    
                case "電話献立":
                    reply_flex_message(reply_token, "クールを選択", tel_select)
                    
                case "電話":
                    reply_two_message(reply_token, "THE ANAHEIMER KITCHEN", "0252652220", tel_message)
                    
                case "今日のお弁当の数":
                    # 今日の日付を取得
                    today = now().date()
                    
                    # 今日の配達数（出席しているユーザー数）をカウント
                    delivery_count = Attendance.objects.filter(day__date=today, is_present=True).count()
                    
                    # 結果を返信
                    reply_message(reply_token, f"今日のお弁当の数: {delivery_count}個")
                    
                case "全員の予定":
                    reply_flex_message(reply_token, "クールを選択", cool_select_cal)
                    
                case "全員の金額":
                    reply_flex_message(reply_token, "クールを選択", cool_select_sum)
                    
                case _:
                    # もしユーザーがまだ登録されていなければ、登録する
                    nickname = message
                    user = User.objects.filter(line_id=user_id).first()
                    if not user:
                        User.objects.create(line_id=user_id, name=nickname)
                        reply_message(reply_token, f"こんにちは、{nickname}さん！登録が完了しました。これからお弁当管理ができます。")
                    else:
                        # すでに登録されている場合は、登録された名前を返す
                        reply_message(reply_token, f"{user.name}さん、実習お疲れ様です！")

    return JsonResponse({"status": "ok"})

# リプライメッセージを送信する関数
def reply_message(reply_token, message):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"}
    
    data = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post(url, headers=headers, json=data)
    return response

# Flex_Messageを送信する関数
def reply_flex_message(reply_token, alt_text, flex_message):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"}
    
    data = {
        "replyToken": reply_token,
        "messages": [{
            "type": "flex",
            "altText": alt_text,
            "contents": flex_message
        }]
    }
    response = requests.post(url, headers=headers, json=data)
    return response

# ２つのリプライを送信する関数
def reply_two_message(reply_token, alt_text, message, flex_message):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"}
    
    data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text", 
                "text": message
            },
            {
                "type": "flex",
                "altText": alt_text,
                "contents": flex_message
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    return response

# 画像を送信する関数
def reply_image_message(reply_token, message, image_url, thumbnail_url):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"}
    
    data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text", 
                "text": message
            },
            {
                "type": "image",
                "originalContentUrl": image_url,
                "previewImageUrl": thumbnail_url
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    return response

# ローディングアニメーションの関数
def start_loading_animation(user_id):
    url = "https://api.line.me/v2/bot/chat/loading/start"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "chatId": user_id,
        "loadingSeconds": 5
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.json()
