#pid controller demo


from pid_new2 import pid
from errorcalc import error

myerror = error()
myerror.vaerror(receiver,gyro) #send the receiver and gyro reading in dps to the function vaerror
error = myerror.error_calc()
mypid = pid()
mypid.create_variables(kp,ki,kd,max_thresh)   #define the values of kp,ki,kd,max_thresh
#at the first time we have to send the value of previous_error=0 and i_error=0 and then update their values 
output,i_error,previous_error = mypid.pid_calc(error,previous_error,i_error)
previous_error = error



