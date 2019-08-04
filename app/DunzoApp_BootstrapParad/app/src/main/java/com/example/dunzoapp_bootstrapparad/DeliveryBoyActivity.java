package com.example.dunzoapp_bootstrapparad;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;
import org.json.JSONException;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;

import javax.net.ssl.HttpsURLConnection;

public class DeliveryBoyActivity extends AppCompatActivity {

    private final int MY_CAMERA_PERMISSION_CODE = 1;
    private final int GALLERY_PERMISSION_CODE = 2;
    private final int CAMERA_REQUEST = 2;
    private ImageView imageViewUploadedImage = null;
    private ImageView buttonUploadIcon = null;
    private ImageView buttonCaptureIcon = null;
    private Uri outputFileUri;
    private InputStream inputStream;
    public static final int PICTURE_ACTIVITY = 35434;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_delivery_boy);

        buttonUploadIcon = findViewById(R.id.buttonUploadIcon);
        buttonCaptureIcon = findViewById(R.id.buttonCaptureIcon);
        imageViewUploadedImage = findViewById(R.id.imageViewUploadedImage);


        buttonUploadIcon.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                    requestPermissions(new String[]{Manifest.permission.CAMERA}, MY_CAMERA_PERMISSION_CODE);
                } else {
                    Intent cameraIntent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
                    startActivityForResult(cameraIntent, CAMERA_REQUEST);
                }
            }
        });

        buttonCaptureIcon.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                if(checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED){
                    requestPermissions(new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, GALLERY_PERMISSION_CODE);

                }else{
                    startActivityForResult(new Intent(Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.INTERNAL_CONTENT_URI), GALLERY_PERMISSION_CODE);
                }
            }

        });
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == MY_CAMERA_PERMISSION_CODE) {
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "camera permission granted", Toast.LENGTH_LONG).show();
                /*Intent cameraIntent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
                startActivityForResult(cameraIntent, CAMERA_REQUEST);*/

                boolean mExternalStorageAvailable = false;
                boolean mExternalStorageWriteable = false;
                String state = Environment.getExternalStorageState();

                if (Environment.MEDIA_MOUNTED.equals(state)) {
                    // We can read and write the media
                    mExternalStorageAvailable = mExternalStorageWriteable = true;
                } else if (Environment.MEDIA_MOUNTED_READ_ONLY.equals(state)) {
                    // We can only read the media
                    mExternalStorageAvailable = true;
                    mExternalStorageWriteable = false;
                } else {
                    // Something else is wrong. It may be one of many other states, but all we need
                    //  to know is we can neither read nor write
                    mExternalStorageAvailable = mExternalStorageWriteable = false;
                }

                if (mExternalStorageAvailable && mExternalStorageWriteable) {
                    Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE); // Normally you would populate this with your custom intent.
                    File file = new File(Environment.getExternalStorageDirectory(), "imagefile.jpg");
                    outputFileUri = Uri.fromFile(file);
                    cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, outputFileUri);
                    startActivityForResult(cameraIntent, PICTURE_ACTIVITY);
                }
            } else {
                Toast.makeText(this, "camera permission denied", Toast.LENGTH_LONG).show();
            }
        }
        if(requestCode == GALLERY_PERMISSION_CODE) {
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "camera permission granted", Toast.LENGTH_LONG).show();
                Intent galleryIntent = new Intent(Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.INTERNAL_CONTENT_URI);
                startActivityForResult(galleryIntent, CAMERA_REQUEST);
            }
        }

    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        Toast.makeText(this, "hahaha..", Toast.LENGTH_LONG).show();
        if (requestCode == CAMERA_REQUEST && resultCode == Activity.RESULT_OK) {
            Toast.makeText(this, "success in retrieving..", Toast.LENGTH_LONG).show();
            buttonCaptureIcon.setVisibility(View.INVISIBLE);
            buttonUploadIcon.setVisibility(View.INVISIBLE);
            Bitmap bitmap = (Bitmap) data.getExtras().get("data");
            imageViewUploadedImage.setImageBitmap(bitmap);
            imageViewUploadedImage.setX(150);
            imageViewUploadedImage.setY(400);
            imageViewUploadedImage.setMaxHeight(300);
            imageViewUploadedImage.setMaxWidth(200);
            AsyncFetch asyncFetch = new AsyncFetch();
            asyncFetch.execute(new Object[]{bitmap});
        }else {
            Toast.makeText(this, "error in retrieving..", Toast.LENGTH_LONG).show();
        }
    }

    public String convertResponseToString(HttpResponse response) throws IllegalStateException, IOException {
        String res = "";
        StringBuffer buffer = new StringBuffer();
        inputStream = response.getEntity().getContent();
        int contentLength = (int) response.getEntity().getContentLength(); //getting content length…..
        Toast.makeText(DeliveryBoyActivity.this, "contentLength : " + contentLength, Toast.LENGTH_LONG).show();
        if (contentLength < 0) {
        } else {
            byte[] data = new byte[512];
            int len = 0;
            try {
                while (-1 != (len = inputStream.read(data))) {
                    buffer.append(new String(data, 0, len)); //converting to string and appending  to stringbuffer…..                    }                }                catch (IOException e)                {                    e.printStackTrace();                }                try                {                    inputStream.close(); // closing the stream…..                }                catch (IOException e)                {                    e.printStackTrace();                }                res = buffer.toString();     // converting stringbuffer to string…..                Toast.makeText(MainActivity.this, "Result : " + res, Toast.LENGTH_LONG).show();                //System.out.println("Response => " +  EntityUtils.toString(response.getEntity()));
                }

            } catch (Exception e) {

            }
        }
        return res;
    }

    private class AsyncFetch extends AsyncTask {

        ProgressDialog pdLoading = new ProgressDialog(DeliveryBoyActivity.this);
        private char ch;
        private String res;
        private Bitmap value=null;

        @Override
        protected void onPreExecute(){
            super.onPreExecute();
            pdLoading.setMessage("\tLoading...");
            pdLoading.setCancelable(false);
            pdLoading.show();
        }

        @Override
        protected Object doInBackground(Object[] params) {
            //Toast.makeText(getActivity(), tabNum+"", Toast.LENGTH_SHORT).show();
            value = (Bitmap)params[0];
            //aa="hiiiiHello";

            try{
                String link = "http://websiteyo.pythonanywhere.com/";
                String data="";
                try {
                    ByteArrayOutputStream stream = new ByteArrayOutputStream();
                    {
                        value.compress(Bitmap.CompressFormat.JPEG, 90, stream);
                    }
                    byte[] byte_arr = stream.toByteArray();
                    String image_str = Base64.encodeToString(byte_arr, 1);
                    data = URLEncoder.encode("upfile", "UTF-8")+"="+URLEncoder.encode(image_str,"UTF-8")+"&"+URLEncoder.encode("work", "UTF-8")+"="+ URLEncoder.encode("retrieve","UTF-8");
                } catch (UnsupportedEncodingException e) {
                    e.printStackTrace();
                }
                //String data = "status=registered";

                URL url = new URL(link);
                HttpURLConnection conn = (HttpURLConnection)url.openConnection();
                conn.setRequestMethod("POST");

                conn.setDoOutput(true);
                OutputStreamWriter wr = new OutputStreamWriter(conn.getOutputStream());
                wr.write(data);
                wr.flush();

                BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                String sb = "";
                String line = null;
                // Read Server Response

                int c = 1;
                //String name="", address="", phone="", comments="";
                while((line = rd.readLine()) != null) {
                    //sb.append(line);
                    sb = sb+line;
                    //break;
                }
                //aa=sb+"    "+sb.length();
                res=sb;
                return sb;

            } catch(Exception e){
                return new String("Exception: " + e.getMessage());
            }
        }

        @Override
        protected void onPostExecute(Object result){
            pdLoading.hide();
            Log.i("result>>>>>>>",result.toString());
        }

    }
}