from client import AskSageClient

client = AskSageClient('nicolas@after-mouse.com', '3912492342449027ad4d5d25b705420a8ddba9a5a6ce46452da143d31e0e3f94')

ret = client.query_with_file('who is Nic Chaillan?')
print(ret)

ret = client.query_with_file('what is this file about?', file='C:/Users/NicolasChaillan/OneDrive/Companies/AskSage/Marketing/Ask Sage - Case Study Veteran Guardian.pdf')
print(ret)