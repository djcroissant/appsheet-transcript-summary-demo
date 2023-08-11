export PROJECT=$(gcloud config get-value project)
export LOCATION=us-west1
export NAME=transcriptsvc

gcloud builds submit --tag "us.gcr.io/$PROJECT/$NAME"

gcloud run deploy $NAME --image us.gcr.io/$PROJECT/$NAME \
    --platform managed --project $PROJECT \
    --min-instances=1 \
    --region $LOCATION --allow-unauthenticated \
    --set-env-vars GCLOUD_PROJECT="$PROJECT"
