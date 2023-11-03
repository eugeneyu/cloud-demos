
First deploy the Llama2 70B model to GKE cluster following this guide.
https://github.com/GoogleCloudPlatform/ai-on-gke/tree/main/tutorials/serving-llama2-70b-on-l4-gpus

Then expose it with a GKE service.

kubectl apply -f frontend/llama-front-lb-svc-new.yaml

To build and deploy the front-end UI to GCP Cloud Run, run the following commands.

PROJECT_ID=eugene-lab-general

cd frontend
gcloud builds submit --tag us-central1-docker.pkg.dev/$PROJECT_ID/genai-cloud-run-demo/llama-bot
gcloud run deploy llama-bot --image us-central1-docker.pkg.dev/$PROJECT_ID/genai-cloud-run-demo/llama-bot --cpu 4 --memory 16G --timeout=10m --no-cpu-throttling --region us-central1 --port 7680

Finally open the link of the Cloud Run app in the browser and ask questions.