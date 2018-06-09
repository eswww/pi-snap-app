#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/gpio.h>       // Required for the GPIO functions
#include <linux/interrupt.h>  // Required for the IRQ code
#include <linux/fs.h>
#include <linux/cdev.h>

MODULE_LICENSE("GPL");

#define DEV_NAME "btn_Dev"

#define BTN0    26

static int btn_value = -1;
static int irq_num0;
static int btn_open(struct inode *inode, struct file *file) {
        printk("btn open\n");
        return 0;
}

static int btn_release(struct inode *inode, struct file *file) {
        printk("btn release\n");
        return 0;
}

struct file_operations btn_fops = {
    .open = btn_open,
    .release = btn_release,
};

static irqreturn_t btn_isr(int irq, void* dev_id) {
        btn_value = 1;
        printk("button push : %d\n",gpio_get_value(BTN0));
        return IRQ_HANDLED;
}

static dev_t dev_num;
static struct cdev *cd_cdev;

static int __init office_init(void) {
        int ret;

        printk("Init Module\n");

        alloc_chrdev_region(&dev_num, 0, 1, DEV_NAME);
        cd_cdev = cdev_alloc();
        cdev_init(cd_cdev, &btn_fops);
        cdev_add(cd_cdev, dev_num, 1);

        gpio_request_one(BTN0, GPIOF_IN, "btn0");
        irq_num0 = gpio_to_irq(BTN0);
        ret = request_irq(irq_num0, btn_isr, IRQF_TRIGGER_FALLING, "btn0_irq", NULL);
        if(ret) {
                printk(KERN_ERR "Unable to request IRQ: %d\n",ret);
                free_irq(irq_num0, NULL);
        }
        return 0;
}

static void __exit office_exit(void) {
        printk("Exit Module\n");

        //del_timer(&break_timer);

        free_irq(irq_num0,NULL);
        //free_irq(irq_num1,NULL);
        gpio_free(BTN0);

	cdev_del(cd_cdev);
	unregister_chrdev_region(dev_num,1);
}

module_init(office_init);
module_exit(office_exit);