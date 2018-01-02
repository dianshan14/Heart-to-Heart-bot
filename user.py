from telegram import Update
class user_msg():
  def __init__(self, update):
    self.msg = update.message
    self.date = self.msg.date
    self.text = self.msg.text
    self.photo = self.msg.photo
    self.user_id = self.msg.from_user.id
    self.name = "%s %s"%(self.msg.from_user.first_name, self.msg.from_user.last_name)

    self.state = 'user'
    
  def get_name(self):
    return self.name

  def get_id(self):
    return self.user_id

  def get_text(self):
    return self.text

  def get_date(self):
    return self.date


def user_handler(user_msg, update, machine):
    print("From: %s %s, Text is: %s"%(update.message.chat.first_name,\
    update.message.chat.last_name, update.message.text))

    user_state = ""
    condition = True
    if user_msg.user_id not in machine.id_list:
        machine.id_list.append(user_msg.user_id)
        machine.user_list.append(user_msg)
        user_state = user_msg.state
    else:
        for i in range(len(machine.id_list)):
            if machine.id_list[i] == user_msg.user_id:
                user_state = machine.user_list[i].state
                machine.user_list[i] = user_msg
                condition = False
                break
    if condition:
        machine.user_list[len(machine.user_list)-1].state = "riddle"
        machine.back_user()
        machine.get_riddle(update)
    else:
        if user_state is "user":
            machine.user_list[i].state = "riddle"
            machine.back_user()
            machine.get_riddle(update)
        elif user_state is "riddle":
            machine.user_list[i].state = "answer_riddle"
            #machine.to_riddle()
            machine.get_riddle_answer(update)
            machine.user_list[i].state = "user" # 暫時先回去
        else:
            update.message.reply_text("Something error happen, Please try again")
        