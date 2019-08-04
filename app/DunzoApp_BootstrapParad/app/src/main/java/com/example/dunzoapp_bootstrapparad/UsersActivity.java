package com.example.dunzoapp_bootstrapparad;

import androidx.appcompat.app.AppCompatActivity;

import android.app.SearchManager;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.ArrayList;

import javax.net.ssl.HttpsURLConnection;

public class UsersActivity extends AppCompatActivity {

    private InputStream inputStream;
    TextView textView;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_users);
        textView = findViewById(R.id.text);
        // Get the intent, verify the action and get the query
        Intent intent = getIntent();
        if (Intent.ACTION_SEARCH.equals(intent.getAction())) {
            String query = intent.getStringExtra(SearchManager.QUERY);
            ArrayList nameValuePairs = new ArrayList();
            nameValuePairs.add(new BasicNameValuePair("searchString", query));

            try {
                HttpClient httpclient = new DefaultHttpClient();
                final String URL = "http://192.168.43.170:5000/searchProducts?searchString="+query;
                HttpGet httpGet = new HttpGet(URL);
               /* HttpPost httppost = new HttpPost(URL);
                httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));*/
                HttpResponse response = httpclient.execute(httpGet);
                String stringResponse = convertResponseToString(response);
                Toast.makeText(UsersActivity.this, "Response " + stringResponse, Toast.LENGTH_LONG).show();
                textView.setText(stringResponse);
            } catch (Exception e) {
                Toast.makeText(UsersActivity
                        .this, "ERROR " + e.getMessage(), Toast.LENGTH_LONG).show();
                System.out.println("Error in http connection " + e.toString());
                e.printStackTrace();
            }

        }
    }

    public String convertResponseToString(HttpResponse response) throws IllegalStateException, IOException {
        String res = "";
        StringBuffer buffer = new StringBuffer();
        inputStream = response.getEntity().getContent();
        int contentLength = (int) response.getEntity().getContentLength(); //getting content length…..
        Toast.makeText(UsersActivity.this, "contentLength : " + contentLength, Toast.LENGTH_LONG).show();
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
}
