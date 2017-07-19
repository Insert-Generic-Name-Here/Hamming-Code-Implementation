## Synopsis

This is python/sage socket made for testing the effects of the well known Hamming code. 

## Specifics

It's built around two sockets that exchange messages , coded using the aformentioned code. Random errors are being added to every word that is sent , in order to observe the results of the attempt to decode the messages. Knowing that the Hamming code is a **SECDED** code , only *one* error can be corrected and a max of *two* errors can be detected in a single word. It's file is sent in a **.json** form and comes with a checksum that is used by the script in order to determine the state of the decoded message. Also a different script has been added in order to calculate the entropy of the initial and the encoded message.

## Input and how to use 

To execute the Server Socket run the sage server script with the parameters of **q r n** where:
q: The Order of the Galois Field 
r: The Order of the Hamming Code 
n: The Maximum Noise to add to the Encoded Messages **NOTE**: the noise is selected randomly, in the integer set [0, n]
*WHILE* having the client socket open in order to recieve the message .

## Contributors

We are students at the University of Piraeus and this code is for a class project. 
The contributors are :
* Andreas Tritsarolis
* Giorgos Theodoropoulos
* Giorgos Gegiannis
