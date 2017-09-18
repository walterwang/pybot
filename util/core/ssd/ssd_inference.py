import numpy as np
import tensorflow as tf

slim = tf.contrib.slim

import sys

sys.path.append('/home/walter/Documents/others_git/SSD-Tensorflow/')
from nets import ssd_vgg_512, ssd_common, np_methods
from preprocessing import ssd_vgg_preprocessing
from notebooks import visualization

# '/home/walter/Documents/others_git/SSD-Tensorflow/checkpoints/rocks/rock_model.ckpt'
class SSD(object):
    def __init__(self,
                 ckpt_filename,
                 n_classes):
        gpu_options = tf.GPUOptions(allow_growth=True)
        config = tf.ConfigProto(log_device_placement=False, gpu_options=gpu_options)
        self.isess = tf.Session(config=config)

        # Input placeholder.
        net_shape = (512, 512)
        data_format = 'NHWC'
        self.img_input = tf.placeholder(tf.uint8, shape=(None, None, 3))
        # Evaluation pre-processing: resize to SSD net shape.
        image_pre, labels_pre, bboxes_pre, self.bbox_img = ssd_vgg_preprocessing.preprocess_for_eval(
            self.img_input, None, None, net_shape, data_format, resize=ssd_vgg_preprocessing.Resize.WARP_RESIZE)
        self.image_4d = tf.expand_dims(image_pre, 0)

        # Define the SSD model.
        reuse = True if 'ssd_net' in locals() else None
        ssd_net = ssd_vgg_512.SSDNet()
        with slim.arg_scope(ssd_net.arg_scope(data_format=data_format)):
            self.predictions, self.localisations, _, _ = ssd_net.net(self.image_4d, is_training=False, reuse=reuse)

        # Restore SSD model.

        # ckpt_filename = '../checkpoints/VGG_VOC0712_SSD_300x300_ft_iter_120000.ckpt'
        self.isess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(self.isess, ckpt_filename)

        # SSD default anchor boxes.
        self.ssd_anchors = ssd_net.anchors(net_shape)
        self.num_classes = n_classes


    # Main image processing routine.
    def process_image(self, img, select_threshold, nms_threshold=.02, net_shape=(512, 512)):
        # Run SSD network.
        rimg, rpredictions, rlocalisations, rbbox_img = self.isess.run([self.image_4d, self.predictions, self.localisations, self.bbox_img],
                                                                  feed_dict={self.img_input: img})

        # Get classes and bboxes from the net outputs.
        rclasses, rscores, rbboxes = np_methods.ssd_bboxes_select(
            rpredictions, rlocalisations, self.ssd_anchors,
            select_threshold=select_threshold, img_shape=net_shape, num_classes = self.num_classes, decode=True)

        rbboxes = np_methods.bboxes_clip(rbbox_img, rbboxes)
        rclasses, rscores, rbboxes = np_methods.bboxes_sort(rclasses, rscores, rbboxes, top_k=400)
        rclasses, rscores, rbboxes = np_methods.bboxes_nms(rclasses, rscores, rbboxes, nms_threshold=nms_threshold)
        # Resize bboxes to original image shape. Note: useless for Resize.WARP!
        rbboxes = np_methods.bboxes_resize(rbbox_img, rbboxes)
        return rclasses, rscores, rbboxes



    def get_objects(self, sct, osclient, object_id ="all", select_threshold=0.6, get_closest = True):
        img = np.array(sct.grab(osclient.box))[:, :, :-1]
        img = np.array(img)
        rcenter = []
        rclasses, rscores, rbboxes = self.process_image(img, select_threshold= select_threshold)
        for ind, box in enumerate(rbboxes):
            topleft = (int(box[1] * img.shape[1]), int(box[0] * img.shape[0]))
            botright = (int(box[3] * img.shape[1]), int(box[2] * img.shape[0]))

            c = (int((botright[0] + topleft[0]) / 2), int((botright[1] + topleft[1]) / 2))
            if object_id == "all":
                rcenter.append(c)
            elif rclasses[ind] in object_id:
                rcenter.append(c)
        print('unsorted ceters', rcenter)
        if get_closest:
            rcenter.sort(key=lambda p: (p[0] - 259) ** 2 + (p[1] - 169) ** 2)
            print('sorted centers', rcenter)

        return rclasses, rbboxes, rcenter