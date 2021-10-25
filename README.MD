# Technical Test Prosa.ai Interview - Khisby Al Ghofari  

### Live Preview
Telegram Username Chatbot @KhisoftBot
Web Chatbot http://khisoft.online:88

### How to run Docker
run using command   
```sudo docker-compose up -d --no-deps --build```

if you have problem with ERR_CONNECTION_RESET
run using command   
```sudo docker run --network host -d prosaai_web```

Generate certbot ssl
```certbot certonly --standalone -d telegram-prosaai.khisoft.online --staple-ocsp -m khisby@gmail.com --agree-tos```

Check port used
```netstat -tulnp```