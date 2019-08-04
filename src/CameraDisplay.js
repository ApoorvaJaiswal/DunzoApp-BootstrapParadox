import React, {Component} from 'react';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  StatusBar,
  Dimensions
} from 'react-native';
import { AppRegistry, Image } from 'react-native';
import { RNCamera } from 'react-native-camera';
const { width: winWidth, height: winHeight } = Dimensions.get('window');

export default class CameraDisplay extends React.Component {
  camera = null;

    async componentDidMount() {
        //const camera = await Permissions.askAsync(Permissions.CAMERA);
        //const audio = await Permissions.askAsync(Permissions.AUDIO_RECORDING);
        //const hasCameraPermission = (camera.status === 'granted' && audio.status === 'granted');

        //this.setState({ hasCameraPermission });
    };


  render() {
    const styles = StyleSheet.create({
      preview: {
          height: winHeight,
          width: winWidth,
          position: 'absolute',
          left: 0,
          top: 0,
          right: 0,
          bottom: 0,
      }
    });

    return (
        <View>
            <RNCamera ref={ref => {this.camera = ref;}} style={{flex: 1,width: '100%',}}>
              
            </RNCamera>
        </View>
    );
  }
  }

  AppRegistry.registerComponent('DunzoApp_BootstrapParadox', () => CameraDisplay);