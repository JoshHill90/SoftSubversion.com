

# contact forms emails -------------------------------------------------------------------------------

# auto reply to contact request

contact_request_body = """
Hi user_name,

Thank you for reaching out! I've received your message regarding user_subject, and I'll be sure to get back to you shortly.
I'm excited to discuss your photography needs and collaborate with you to create stunning visuals that capture your unique style.
In the meantime, please keep an eye on your inbox for my response. If you don't receive a follow-up email from me within 24 hours, 
please check your spam folder, just in case.

Looking forward to connecting with you soon!

Best regards,
Carly


SoftSubversion.com
"""

# contact form filled out 

contact_alart_body = """ 
        Subject: user_subject

        From: user_email - Name: user_name

        Message:
            body


"""

# client and project emails -------------------------------------------------------------------------------


# client requesing a new project 
project_request_notice_body = """

Project Request!!!
From: client_name - ID#: user_id
Project Name project_name
Requested scope  scope
Requested date  date_selected
Requested Location type location
Details details
          
"""

# notice to clinet of new comment on project request

owner_post_comment_ = """
Hey user_name,

A new comment has been posted for your project reeequest project_name.

owner commented:

        comment

link


"""
owner_post_comment_body = str(owner_post_comment_)