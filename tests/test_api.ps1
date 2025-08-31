# PowerShell script to test your Flask trading engine API
# Save as test_api.ps1 and run in PowerShell after starting your server

Write-Host "Add buy order (BTCUSD)"
$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/order" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"order_id":"1","symbol":"BTCUSD","side":"buy","price":100,"quantity":1,"user_id":"u1"}'
$response.Content

Write-Host "Add sell order (BTCUSD)"
$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/order" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"order_id":"2","symbol":"BTCUSD","side":"sell","price":101,"quantity":2,"user_id":"u2"}'
$response.Content

Write-Host "Get L2 depth (BTCUSD)"
$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/depth?symbol=BTCUSD" -Method GET
$response.Content

Write-Host "Match orders (BTCUSD)"
$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/match" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"symbol":"BTCUSD"}'
$response.Content

Write-Host "Get user PnL (u1, BTCUSD)"
$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/pnl?symbol=BTCUSD&user_id=u1" -Method GET
$response.Content

Write-Host "Get user PnL (u2, BTCUSD)"
$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/pnl?symbol=BTCUSD&user_id=u2" -Method GET
$response.Content

Write-Host "Add buy order (ETHUSD)"
$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/order" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"order_id":"3","symbol":"ETHUSD","side":"buy","price":200,"quantity":1,"user_id":"u3"}'
$response.Content

Write-Host "Get L2 depth (ETHUSD)"
$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/depth?symbol=ETHUSD" -Method GET
$response.Content
