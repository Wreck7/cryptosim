from supabase import create_client


url = 'https://cnlomrmitfonwvxyaycj.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNubG9tcm1pdGZvbnd2eHlheWNqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA0NDM4ODEsImV4cCI6MjA2NjAxOTg4MX0.P1Aw2rrDdLl1f-Ya3sFS6L3gVuXeByoOwrUB2rXTVOE'

db = create_client(url, key)