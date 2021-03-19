import pandas as pd
contacts_df = pd.read_json("contacts.json") #columns: Id(unique ticket), Email, Phone, Contacts, OrderId

# print(contacts_df.head())

contacts_df["userid"] = "" #columns: Id(unique ticket), Email, Phone, Contacts, OrderId, User

# print(contacts_df.head())

user_exists = False
new_userid = 0


# how to get the Contacts of the ticket with OrderId=="JsORSKHmzWlRvSNKUTVofoPkZ"
# contacts = contacts_df.loc[contacts_df["OrderId"] =="JsORSKHmzWlRvSNKUTVofoPkZ"]["Contacts"].iloc[0]
# contacts = contacts_df.loc[contacts_df["OrderId"] =="JsORSKHmzWlRvSNKUTVofoPkZ"]["OrderId"].values[0]

# how to get total contact count of the tickets with Email=="hUKlNubtVcCkFHr@qq.com"
# contact_count = contacts_df.loc[contacts_df["Email"]=="hUKlNubtVcCkFHr@qq.com"]["Contacts"].sum()

# how to select rows based on the value of one of their columns
# same_user = contacts_df[contacts_df["Email"] == "hUKlNubtVcCkFHr@qq.com"]
# number_of_rows = same_user.shape[0]


# iterate through each row in the df, if the current row's deets (email, phone, orderid) have appeared before the current row, then it means its an existing user and should have the same userid
# if not then give it the next unique userid
for i in range(contacts_df.shape[0]):
    # user_exists = False
    if (i==0):
        contacts_df.loc[i, "userid"] = new_userid
        new_userid += 1
    else:
        if (contacts_df.loc[i, "Email"] in contacts_df.loc[:i-1, "Email"].values):
            #get the existing userid using Email
            userid = contacts_df.loc[contacts_df["Email"]==contacts_df.loc[i, "Email"]]["userid"].values[0]
            contacts_df.loc[i, "userid"] = userid
        elif (contacts_df.loc[i, "Phone"] in contacts_df.loc[:i-1, "Phone"].values):
            #get the existing userid using Phone
            userid = contacts_df.loc[contacts_df["Phone"]==contacts_df.loc[i, "Phone"]]["userid"].values[0]
            contacts_df.loc[i, "userid"] = userid
        elif (contacts_df.loc[i, "OrderId"] in contacts_df.loc[:i-1, "OrderId"].values):
            #get existing userid using OrderId
            userid = contacts_df.loc[contacts_df["OrderId"]==contacts_df.loc[i, "OrderId"]]["userid"].values[0]
            contacts_df.loc[i, "userid"] = userid
        else:
            #user not an existing user so give it the next unique userid
            contacts_df.loc[i, "userid"] = new_userid
            new_userid += 1

print(contacts_df.head())

# after getting the df with all the userids, sort using userid, Id (contacts_df.sort_values(by=["userid","Id"]))
# then iterate through all user ids and get the string of ids in order + the total contacts count
# then replace the userid column values with this string + total contacts count
contacts_df = contacts_df.sort_values(by=["userid", "Id"])
id = contacts_df.columns.get_loc("Id")
for j in range(new_userid):
    contact_count=0
    ticket_trace=""
    same_user = contacts_df[contacts_df["userid"]==j]
    for m in range (same_user.shape[0]):
        ticket_trace += str(same_user.iloc[m, id]) + "-"
    ticket_trace=ticket_trace[:-1]
    contact_count = contacts_df.loc[contacts_df["userid"]==j]["Contacts"].sum()
    ticket_trace_contact = ticket_trace + "/" + str(contact_count)
    contacts_df["userid"] = contacts_df["userid"].replace(j, ticket_trace_contact)
    # print(same_user)
    # print(ticket_trace_contact)


# after doing this for all userids, sort using Id, then rename the Id column to ticket_id, and rename the userid column to ticket_trace/contact
# then finally drop the Email, Phone, Contacts columns and output to csv file
contacts_df = contacts_df.sort_values(by=["Id"])
contacts_df.rename(columns={"userid": "ticker_trace/contact", "Id": "ticket_id"})
contacts_df.drop(["Email", "Phone", "Contacts"])

contacts_df.to_csv("output")
