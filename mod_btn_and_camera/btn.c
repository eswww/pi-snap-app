#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/gpio.h>       // Required for the GPIO functions
#include <linux/interrupt.h>  // Required for the IRQ code
#include <linux/kobject.h>    // Using kobjects for the sysfs bindings
#include <linux/init.h>
#include <linux/kthread.h>
#include <linux/errno.h>
#include <linux/types.h>
#include <linux/netdevice.h>
#include <linux/ip.h>
#include <linux/in.h>
#include <linux/delay.h>

#define DEFAULT_PORT 2325
#define CONNECT_PORT 23
#define MODULE_NAME "m_server"
#define INADDR_SEND INADDR_LOOPBACK

#define gpioButton 115;
#define  DEBOUNCE_TIME 200    ///< The default bounce time -- 200ms

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("test btn.ko and camera.py");
MODULE_VERSION("0.1");

struct kthread_t
{
        struct task_struct *thread;
        struct socket *sock;
        struct sockaddr_in addr;
        int running;
};

struct kthread_t *kthread = NULL;

static bool isRising = 1;                   ///< Rising edge is the default IRQ property
static int  numberPresses = 0;            ///< For information, store the number of button presses for test.
module_param(isRising, bool, S_IRUGO);      ///< Param desc. S_IRUGO can be read/not changed
MODULE_PARM_DESC(isRising, " Rising edge = 1 (default), Falling edge = 0");  ///< parameter description

//irq handle_button
static irq_handler_t  ebbgpio_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs);
static int ksocket_send(struct socket *sock, struct sockaddr_in *addr, unsigned char *buf, int len);

static irq_handler_t ebbgpio_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs){

   printk(KERN_INFO "EBB Button: The button state is currently: %d\n", gpio_get_value(gpioButton));
   numberPresses++;                     // Global counter, will be outputted when the module is unloaded
   return (irq_handler_t) IRQ_HANDLED;  // Announce that the IRQ has been handled correctly
}
static void ksocket_start(void)
{
        int size, err;
        int bufsize = 10;
        unsigned char buf[bufsize+1];

        /* kernel thread initialization */
        lock_kernel();
        current->flags |= PF_NOFREEZE;

        /* daemonize (take care with signals, after daemonize() they are disabled) */
        daemonize(MODULE_NAME);
        allow_signal(SIGKILL);
        unlock_kernel();
        kthread->running = 0;

        /* create a socket */
        if ( ( (err = sock_create(AF_INET, SOCK_DGRAM, IPPROTO_UDP, &kthread->sock)) < 0) )
        {
                printk(KERN_INFO MODULE_NAME": Could not create a datagram socket, error = %d\n", -ENXIO);
                goto out;
        }

        memset(&kthread->addr, 0, sizeof(struct sockaddr));
        kthread->addr.sin_family      = AF_INET;

        kthread->addr.sin_addr.s_addr      = htonl(INADDR_ANY);

        kthread->addr.sin_port      = htons(DEFAULT_PORT);

        if ( ( (err = kthread->sock->ops->bind(kthread->sock, (struct sockaddr *)&kthread->addr, sizeof(struct sockaddr) ) ) < 0))
        {
                printk(KERN_INFO MODULE_NAME": Could not bind or connect to socket, error = %d\n", -err);
                goto close_and_out;
        }

        printk(KERN_INFO MODULE_NAME": listening on port %d\n", DEFAULT_PORT);

        /* main loop */
        for (;;)
        {

                if (signal_pending(current))
                        break;

                if (size < 0)
                        printk(KERN_INFO MODULE_NAME": error getting datagram, sock_recvmsg error = %d\n", size);
                else
                {
                        printk(KERN_INFO MODULE_NAME": received %d bytes\n", size);
                        ksocket_send(kthread->sock, &kthread->addr, numberPresses, sizeof(int));
                }
        }

close_and_out:
        sock_release(kthread->sock);
        kthread->sock = NULL;

out:
        kthread->thread = NULL;
        kthread->running = 0;
}
static int ksocket_send(struct socket *sock, struct sockaddr_in *addr, int numberPresses, int len) {
        struct msghdr msg;
        struct iovec iov;
        mm_segment_t oldfs;
        int size = 0;

        if (sock->sk==NULL)
           return 0;

        iov.iov_base = (int *)iov.iov_base;
        iob.iov_base =  &numberPresses
        iov.iov_len = len;

        msg.msg_flags = 0;
        msg.msg_name = addr;
        msg.msg_namelen  = sizeof(struct sockaddr_in);
        msg.msg_control = NULL;
        msg.msg_controllen = 0;
        msg.msg_iov = &iov;
        msg.msg_iovlen = 1;
        msg.msg_control = NULL;

        oldfs = get_fs();
        set_fs(KERNEL_DS);
        size = sock_sendmsg(sock,&msg,len);
        set_fs(oldfs);
        return size;
}

static int __init ebbButton_init(void){
   int result = 0;
   unsigned long IRQflags = IRQF_TRIGGER_RISING;      // The default is a rising-edge interrupt

   printk(KERN_INFO "EBB Button: Initializing the EBB Button\n");

   // create the kobject sysfs entry at /sys/ebb -- probably not an ideal location!
			                    // the bool argument prevents the direction from being changed
   gpio_request(gpioButton, "sysfs");       // Set up the gpioButton
   gpio_direction_input(gpioButton);        // Set the button GPIO to be an input
   gpio_set_debounce(gpioButton, DEBOUNCE_TIME); // Debounce the button with a delay of 200ms
   gpio_export(gpioButton, false);          // Causes gpio115 to appear in /sys/class/gpio
			                    // the bool argument prevents the direction from being changed

   // Perform a quick test to see that the button is working as expected on LKM load
   printk(KERN_INFO "EBB Button: The button state is currently: %d\n", gpio_get_value(gpioButton));

   /// GPIO numbers and IRQ numbers are not the same! This function performs the mapping for us
   irqNumber = gpio_to_irq(gpioButton);
   printk(KERN_INFO "EBB Button: The button is mapped to IRQ: %d\n", irqNumber);

   if(!isRising){                           // If the kernel parameter isRising=0 is supplied
      IRQflags = IRQF_TRIGGER_FALLING;      // Set the interrupt to be on the falling edge
   }
   // This next call requests an interrupt line
   result = request_irq(irqNumber,             // The interrupt number requested
                        (irq_handler_t) ebbgpio_irq_handler, // The pointer to the handler function below
                        IRQflags,              // Use the custom kernel param to set interrupt type
                        "ebb_button_handler",  // Used in /proc/interrupts to identify the owner
                        NULL);                 // The *dev_id for shared interrupt lines, NULL is okay
   return result;
        kthread = kmalloc(sizeof(struct kthread_t), GFP_KERNEL);
        memset(kthread, 0, sizeof(struct kthread_t));

        kthread->thread = kthread_run((void *)ksocket_start, NULL, MODULE_NAME);
        if (IS_ERR(kthread->thread))
        {
                printk(KERN_INFO MODULE_NAME": unable to start kernel thread\n");
                kfree(kthread);
                kthread = NULL;
                return -ENOMEM;
        }   
}
static void __exit ebbButton_exit(void){
   printk(KERN_INFO "EBB Button: The button was pressed %d times\n", numberPresses);

   free_irq(irqNumber, NULL);               // Free the IRQ number, no *dev_id required in this case
   gpio_unexport(gpioButton);               // Unexport the Button GPIO
   gpio_free(gpioButton);                   // Free the Button GPIO
   printk(KERN_INFO "EBB Button: Goodbye from the EBB Button LKM!\n");
   #if 0
           if (kthread->thread==NULL)
                   printk(KERN_INFO MODULE_NAME": no kernel thread to kill\n");
           else 
           {
                   lock_kernel();
                   err = kill_proc(kthread->thread->pid, SIGKILL, 1);
                   unlock_kernel();

                   if (err < 0)
                           printk(KERN_INFO MODULE_NAME": unknown error %d while trying to terminate kernel thread\n",-err);
                   else 
                   {
                           while (kthread->running == 1)
                                   msleep(10);
                           printk(KERN_INFO MODULE_NAME": succesfully killed kernel thread!\n");
                   }
           }
   #endif

           if (kthread->running)
                   kthread_stop(kthread->thread);
           if (kthread->sock != NULL)
           {
                   sock_release(kthread->sock);
                   kthread->sock = NULL;
           }

           kfree(kthread);
           kthread = NULL;

           printk(KERN_INFO MODULE_NAME": module unloaded\n");   
}

module_init(ebbButton_init);
module_exit(ebbButton_exit);