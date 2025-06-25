from supabase import create_client


url = 'https://cnlomrmitfonwvxyaycj.supabase.co' #my database
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNubG9tcm1pdGZvbnd2eHlheWNqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA0NDM4ODEsImV4cCI6MjA2NjAxOTg4MX0.P1Aw2rrDdLl1f-Ya3sFS6L3gVuXeByoOwrUB2rXTVOE'

# url = 'https://kgrpxirvwdgnqsmwgnff.supabase.co' # team database
# key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtncnB4aXJ2d2RnbnFzbXdnbmZmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA3NzU1OTcsImV4cCI6MjA2NjM1MTU5N30.2GKEl_lkltL4IEc9Y0S_QrM9kzT3tzVRFxZ4MlAPx_8'


db = create_client(url, key)