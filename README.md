![alt text](https://github.com/fabiose81/events/blob/master/events.jpg?raw=true)

### For Kubernetes
    service/deploy/service_configmap.yaml
        SENDER_EMAIL: "set your email"
      
    service/deploy/secret.yaml
       SENDER_EMAIL_PASSWORD: "set your googleapi code"
       PS: For Gmail go to https://myaccount.google.com to create your code

    To run containeres(in deploy folder): kubectl apply -f ./
