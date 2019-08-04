/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow
 */

import React, {Component} from 'react';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  StatusBar,
} from 'react-native';

import {
  Header,
  LearnMoreLinks,
  Colors,
  DebugInstructions,
  ReloadInstructions,
} from 'react-native/Libraries/NewAppScreen';
import { whileStatement } from '@babel/types';
import CameraDisplay from './src/CameraDisplay';
import {Dimensions} from 'react-native';

export default class App extends React.Component{
  render(){
    return(
        <CameraDisplay />
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  myButton1:{
    padding: 3,
    height: 20,
    width: 20,  //The Width must be the same as the height
    borderRadius:40, //Then Make the Border Radius twice the size of width or Height   
    backgroundColor:'rgb(102, 153, 153)',
    color: '#fff'
  },
  myButton2:{
    padding: 3,
    height: 20,
    width: 20,  //The Width must be the same as the height
    borderRadius:40, //Then Make the Border Radius twice the size of width or Height   
    backgroundColor:'rgb(255, 153, 51)',
    color: '#fff'
  }
});

//export default App;
