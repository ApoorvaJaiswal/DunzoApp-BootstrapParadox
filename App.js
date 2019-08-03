/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow
 */

import React, {Fragment} from 'react';
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

const App = () => {
  return(
    <View>
      <View style={styles.container}>
          <View style={styles.myButton1} onPress={() => this.props.navigation.navigate('User')}>
            <Text>Circle Button1</Text>
          </View>
      </View>

      <View style={styles.container}>
          <View style={styles.myButton2} onPress={() => this.props.navigation.navigate('User')}>
            <Text>Circle Button2</Text>
          </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  myButton1:{
    padding: 5,
    height: 200,
    width: 200,  //The Width must be the same as the height
    borderRadius:400, //Then Make the Border Radius twice the size of width or Height   
    backgroundColor:'rgb(102, 153, 153)',
    color: '#fff'
  },
  myButton2:{
    padding: 5,
    height: 200,
    width: 200,  //The Width must be the same as the height
    borderRadius:400, //Then Make the Border Radius twice the size of width or Height   
    backgroundColor:'rgb(255, 153, 51)',
    color: '#fff'
  }
});

export default App;
