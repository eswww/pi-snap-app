#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/gpio.h>       // Required for the GPIO functions
#include <linux/interrupt.h>  // Required for the IRQ code

#define gpioButton 26
#define DEBOUNCE_TIME 200    ///< The default bounce time -- 200ms

MODULE_LICENSE("GPL");;
static int irqNumber;
static bool isRising = 1;                   ///< Rising edge is the default IRQ property
static int  numberPresses = 0;            ///< For information, store the number of button presses for test.
module_param(isRising, bool, S_IRUGO);      ///< Param desc. S_IRUGO can be read/not changed
MODULE_PARM_DESC(isRising, " Rising edge = 1 (default), Falling edge = 0");  ///< parameter description

//irq handle_button
static irq_handler_t  ebbgpio_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs);

static irq_handler_t ebbgpio_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs){

   printk(KERN_INFO "button state is currently: %d numberPresses : %d\n", gpio_get_value(gpioButton),numberPresses);
   numberPresses++;                     // Global counter, will be outputted when the module is unloaded
   return (irq_handler_t) IRQ_HANDLED;  // Announce that the IRQ has been handled correctly
}


static int __init ebbButton_init(void){
   int result = 0;
   unsigned long IRQflags = IRQF_TRIGGER_RISING;      // The default is a rising-edge interrupt

   printk(KERN_INFO "EBB Button: Initializing the EBB Button\n");

   gpio_request(gpioButton, "sysfs");       // Set up the gpioButton
   gpio_direction_input(gpioButton);        // Set the button GPIO to be an input
   gpio_set_debounce(gpioButton, 200);      // Debounce the button with a delay of 200ms
   gpio_export(gpioButton, false);   /// GPIO numbers and IRQ numbers are not the same! This function performs the mapping for us
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
}
static void __exit ebbButton_exit(void){
   printk(KERN_INFO "EBB Button: The button was pressed %d times\n", numberPresses);

   free_irq(irqNumber, NULL);               // Free the IRQ number, no *dev_id required in this case

   gpio_free(gpioButton);                   // Free the Button GPIO
   printk(KERN_INFO "EBB Button: Goodbye from the EBB Button LKM!\n");

}

module_init(ebbButton_init);
module_exit(ebbButton_exit);