# JWT-authenticated and event manager

  ⚙️ : Python
  💻 : React(JavaScript)
  🐳 : Docker
  ☸️ : Kubernetes

https://github.com/user-attachments/assets/fb4c1784-6b0b-4f65-bb63-bbd4a588a786

![alt text](https://github.com/fabiose81/events/blob/master/events.jpg?raw=true)

### To run applications by Kubernetes
    service/deploy/service_configmap.yaml
        SENDER_EMAIL: "set your email"
      
    service/deploy/secret.yaml
       SENDER_EMAIL_PASSWORD: "set your googleapi code"
       PS: For Gmail go to https://myaccount.google.com to create your code

    To run containeres(in deploy folder): kubectl apply -f ./
