import numpy as np
import cv2
import time
import argparse
from venv import create
from project_1 import create_app
from werkzeug.utils import secure_filename
from fileinput import filename
import mysql.connector
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from . import db
from .models import Post, Tag, User, Comment, Rating, Downvote
from datetime import datetime, timedelta
import uuid as uuid
import os

from flask_sqlalchemy import SQLAlchemy

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    posts = Post.query.all()
    tags = Tag.query.all()
    
    return render_template("home.html", user=current_user, posts=posts, tags=tags)

@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method =='POST':
        subject = request.form.get('subject')
        content = request.files['content']
        tagString = request.form.get('tag')
        tags = tagString.split(", ")
        print(subject)
        print(content)
        print(tagString)
        print(tags)
        print(current_user)

        posts = Post.query.all()
        date = datetime.now()
        t = timedelta(days=1)
        count = 0

        #Check for all posts that were created by the current user less than 1 day ago.
        for post in posts:
            if (post.author == current_user.username):
                if (date - post.date_created) < t:
                    count = count + 1

        
        if not subject:
            flash('Subject cannot be empty', category='error')
        elif not content:
            flash('Content cannot be left empty', category='error')
        elif count > 2:
            flash('Can not make more than 2 posts per day.', category='error')
        else:
            
            if not tagString:
                # #Inpainting process
                
                # parser = argparse.ArgumentParser()
                
                # # parser.add_argument("-s", "--slice", required=True, help="path to input image")
                # parser.add_argument("-y", "--yolo", help="base path to YOLO directory", default='yolo-coco')

                # parser.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
                # parser.add_argument("-t", "--threshold", type=float, default=0.3, help="threshold when applying non-maxima suppression")
                # parser.add_argument("-r", "--iter", type=int, default=10, help="# of GrabCut iterations (larger value => slower runtime)")
                # parser.add_argument("-a", "--method", type=str, default="telea", choices=["telea", "ns"], help="inpainting algorithm to use")
                # parser.add_argument("-ra", "--radius", type=int, default=3, help="inpainting radius")

                # args = vars(parser.parse_args())

                # # load the COCO class labels our YOLO model was trained on
                # labelsPath = os.path.sep.join(args["yolo"], "coco.names"])
                # LABELS = open(labelsPath).read().strip().split("\n")

                # # initialize a list of colors to represent each possible class label
                # np.random.seed(42)
                # COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype='uint8')

                # # derive the paths to the YOLO weights and model configuration
                # weightsPath = os.path.sep.join(args["yolo"], "yolov3.weights"])
                # configPath = os.path.sep.join(args["yolo"], "yolov3.cfg"])

                # # load our YOLO object detector trained on COCO dataset (80 classes)
                # print("[INFO] loading YOLO from disk...")
                # net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

                # # load our input image and grab its spatial dimensions
                # image = cv2.imread(content)
                # (H, W) = image.shape[:2]


                # # determine only the *output* layer names that we need from YOLO
                # ln = net.getLayerNames()
                # ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

                # # construct a blob from the input image and then perform a forward
                # # pass of the YOLO object detector, giving us our bounding boxes and
                # # associated probabilities
                # blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                #                             swapRB=True, crop=False)
                # net.setInput(blob)
                # start = time.time()
                # layerOutputs = net.forward(ln)
                # end = time.time()

                # # show timing information on YOLO
                # print("[INFO] YOLO took {:.6f} seconds".format(end - start))

                # # initialize our lists of detected bounding boxes, confidences, and
                # # class IDs, respectively
                # boxes = []
                # confidences = []
                # classIDs = []

                # # loop over each of the layer outputs
                # for output in layerOutputs:
                #     # loop over each of the detections
                #     for detection in output:
                #         # extract the class ID and confidence (i.e., probability) of
                #         # the current object detection
                #         scores = detection[5:]
                #         classID = np.argmax(scores)
                #         confidence = scores[classID]
                #         # filter out weak predictions by ensuring the detected
                #         # probability is greater than the minimum probability
                #         if confidence > args["confidence"]:
                #             # scale the bounding box coordinates back relative to the
                #             # size of the image, keeping in mind that YOLO actually
                #             # returns the center (x, y)-coordinates of the bounding
                #             # box followed by the boxes' width and height
                #             box = detection[0:4] * np.array([W, H, W, H])
                #             (centerX, centerY, width, height) = box.astype("int")
                #             # use the center (x, y)-coordinates to derive the top and
                #             # and left corner of the bounding box
                #             x = int(centerX - (width / 2))
                #             y = int(centerY - (height / 2))
                #             # update our list of bounding box coordinates, confidences,
                #             # and class IDs
                #             boxes.append([x, y, int(width), int(height)])
                #             confidences.append(float(confidence))
                #             classIDs.append(classID)

                # # apply non-maxima suppression to suppress weak, overlapping bounding
                # # boxes
                # idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
                #                         args["threshold"])

                # # ensure at least one detection exists
                # if len(idxs) > 0:
                #     print("Object has been found")
                #     # loop over the indexes we are keeping
                #     for i in idxs.flatten():
                #         # extract the bounding box coordinates
                #         (x, y) = (boxes[i][0], boxes[i][1])
                #         (w, h) = (boxes[i][2], boxes[i][3])

                #         # draw a bounding box rectangle and label on the image
                #         color = [int(c) for c in COLORS[classIDs[i]]]

                #         # cv2.rectangle(image, (x, y), (x + w, y + h), color, 2) Don't need this messes with grabcut
                #         text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                #         cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                #                     0.5, color, 2)
                #     print(boxes)
                #     # print(x, y)
                #     # print(w, h)
                #     print(idxs)
                #     # # show the output image
                #     # cv2.imshow("Image", image)
                #     # cv2.waitKey(0)

                #     # rect = [(x, y, x + w, y + h)]
                #     ###### Bird Mask ###
                #     #rect = [(107, 53, 168, 274)] 
                #     # rect =  [(131, 98, 176, 169)]
                #     #### Apple Mask ####
                #     rect = [(389, 170, 39, 40)]
                #     # rect = [(109, 54, 160, 276)]
                #     print(rect)

                #     ####################################################################################################################
                #     # rect = boxes[1]
                #     # rect = [(205, 358, 645, 790), (1213, 447, 525, 815)]

                #     for x in rect:
                #         #####################################################################################

                #         #allocate memory for the
                #         # output mask generated by GrabCut -- this mask should hae the same
                #         # spatial dimensions as the input image
                #         mask = np.zeros(image.shape[:2], dtype="uint8")

                #         # allocate memory for two arrays that the GrabCut algorithm internally
                #         # uses when segmenting the foreground from the background
                #         fgModel = np.zeros((1, 65), dtype="float")
                #         bgModel = np.zeros((1, 65), dtype="float")

                #         # apply GrabCut using the the bounding box segmentation method
                #         start = time.time()
                #         (mask, bgModel, fgModel) = cv2.grabCut(image, mask, x, bgModel,
                #             fgModel, iterCount=args["iter"], mode=cv2.GC_INIT_WITH_RECT)
                #         end = time.time()
                #         print("[INFO] applying GrabCut took {:.2f} seconds".format(end - start))

                #         # the output mask has for possible output values, marking each pixel
                #         # in the mask as (1) definite background, (2) definite foreground,
                #         # (3) probable background, and (4) probable foreground
                #         values = (
                #             # ("Definite Background", cv2.GC_BGD),
                #             # ("Probable Background", cv2.GC_PR_BGD),
                #             # ("Definite Foreground", cv2.GC_FGD),
                #             ("Probable Foreground", cv2.GC_PR_FGD),
                #         )

                #         sampleMask = image
                #         # loop over the possible GrabCut mask values
                #         for (name, value) in values:
                #             # construct a mask that for the current value
                #             print("[INFO] showing mask for '{}'".format(name))
                #             valueMask = (mask == value).astype("uint8") * 255
                #             # display the mask so we can visualize it
                #             cv2.imwrite("assets/masks/mask.png", valueMask)
                #             cv2.imshow(name, valueMask)
                #             cv2.waitKey(0)


                #         # we'll set all definite foreground and probable foreground pixels
                #         # to 0 while definite background and probable background pixels are
                #         # set to 1
                #         BGoutputMask = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD),
                #             1, 0)
                #         # scale the mask from the range [1, 0] to [0, 255]
                #         BGoutputMask = (BGoutputMask * 255).astype("uint8")

                #         # apply a bitwise AND to the image using our mask generated by
                #         # GrabCut to generate our final background extraction
                #         BGoutputMask = cv2.bitwise_and(image, image, mask=BGoutputMask)

                #         FGoutputMask = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD),
                #             0, 1)
                #         # scale the mask from the range [0, 1] to [0, 255]
                #         FGoutputMask = (FGoutputMask * 255).astype("uint8")

                #         # apply a bitwise AND to the image using our mask generated by
                #         # GrabCut to generate our final forground extraction
                #         FGoutputMask = cv2.bitwise_and(image, image, mask=FGoutputMask)

                #         # show the input image followed by the mask and output generated by
                #         # GrabCut and bitwise masking
                #         cv2.imshow("Input", image)
                #         cv2.imshow("Background cutout", BGoutputMask)
                #         cv2.imshow("Foreground cutout", FGoutputMask)
                #         # cv2.imshow("GrabCut Output", output)
                #         cv2.waitKey(0)

                #         # cv2.imwrite('./inpainter/Output/foreground.png', FGoutputMask)
                #         # cv2.imwrite('./inpainter/Output/background.png', BGoutputMask)

                #         # start of inpainting
                #         ################

                #         # initialize the inpainting algorithm to be the Telea et al. method
                #         flags = cv2.INPAINT_TELEA
                #         # check to see if we should be using the Navier-Stokes (i.e., Bertalmio
                #         # et al.) method for inpainting
                #         if args["method"] == "ns":
                #             flags = cv2.INPAINT_NS

                #         # load the (1) input image (i.e., the image we're going to perform
                #         # inpainting on) and (2) the  mask which should have the same input
                #         # dimensions as the input image -- zero pixels correspond to areas
                #         # that *will not* be inpainted while non-zero pixels correspond to
                #         # "damaged" areas that inpainting will try to correct
                #         image = cv2.imread(args["slice"])
                #         mask = cv2.imread("assets/masks/mask.png")
                #         mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

                #         # perform inpainting using OpenCV
                #         output = cv2.inpaint(image, mask, args["radius"], flags=flags)

                #         # show the original input image, mask, and output image after
                #         # applying inpainting
                #         cv2.imshow("Image", image)
                #         cv2.imshow("Mask", mask)
                #         cv2.imshow("Output", output)
                #         cv2.waitKey(0)

                #saves the image
                filename = secure_filename(content.filename)
                mimetype = content.mimetype
                pic_name = str(uuid.uuid1()) + "_" + filename

                content.save(os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name))
                

                print(filename)
                print(mimetype)

                post = Post(subject=subject, content=pic_name, name=filename, mimetype=mimetype, author=current_user.username)
                db.session.add(post)
                db.session.commit()
                flash('Post created', category='success')
                return redirect(url_for('views.home'))
            else:
                post = Post(subject=subject, content=content.read(), name=filename, mimetype=mimetype, author=current_user.username)
                db.session.add(post)
                db.session.commit()
                tags = tagString.split(", ")

                for tag in tags:
                    new_tag = Tag(tag=tag, PostID=post.PostID)
                    db.session.add(new_tag)
                    db.session.commit() 
                flash('Post created', category='success')   
                return redirect(url_for("views.home"))

    return render_template("create_post.html", user=current_user)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(PostID=id).first()

    if not post:
        flash("Post does not exist.", category='error')
        
    elif current_user.username != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')

    return redirect(url_for('views.home'))

@views.route("/posts/<username>")
@login_required
def posts(username):
    
    user = User.query.filter_by(username=username).all()

    if not user:
        flash('User does not exist.', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=username).all()
    tags = Tag.query.all()
    return render_template("posts.html", user=current_user, posts=posts, username=username, tags=tags)

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(PostID=post_id)

        comments = Comment.query.filter_by(post_id=post_id)
        postCommentCount = 0
        for comment in comments:
            if current_user.username == comment.author:
                postCommentCount = postCommentCount + 1
        
        allComments = Comment.query.all()
        date = datetime.now()
        t = timedelta(days=1)
        totalCommentCount = 0

        #Check for all comments that were created by the current user less than 1 day ago.
        for comment in allComments:
            if (comment.author == current_user.username):
                if (date - comment.date_created) < t:
                    totalCommentCount = totalCommentCount + 1
        

        if postCommentCount > 0:
            flash('You cannot make more than 1 comment per post.', category='error')
        elif totalCommentCount > 2:
            flash('You can only make 3 comments per day.', category='error')
        elif post:
            comment = Comment(text=text, author=current_user.username, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')


    return redirect(url_for('views.home'))

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist', category='error')
    elif current_user.username != comment.author and current_user.username != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))

@views.route("/like-post/<postid>", methods=['GET'])
@login_required
def like(postid):
    post = Post.query.filter_by(PostID=postid)
    rating = Rating.query.filter_by(author=current_user.username, post_id=postid,).first()

    if not post:
        flash('Post does not exist.', category='error')
    elif rating:
        db.session.delete(rating)
        db.session.commit()
    else:
        rating = Rating(author=current_user.username, post_id=postid, vote='like')
        db.session.add(rating)
        db.session.commit()

    return redirect(url_for('views.home'))

@views.route("/dislike-post/<postid>", methods=['GET'])
@login_required
def dislike(postid):
    post = Post.query.filter_by(PostID=postid)
    rating = Downvote.query.filter_by(author=current_user.username, post_id=postid,).first()

    if not post:
        flash('Post does not exist.', category='error')
    elif rating:
        db.session.delete(rating)
        db.session.commit()
    else:
        rating = Downvote(author=current_user.username, post_id=postid, vote='dislike')
        db.session.add(rating)
        db.session.commit()

    return redirect(url_for('views.home'))

@views.route('/initialize-db', methods=['GET', 'POST'])
@login_required
def initDB():

    if request.method == 'POST':
        print("Testing passed")
        rejected = True
        response = ''

        try:
            
            mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="pass1234",
            database="users"
            )

            cursor = mydb.cursor()
           
            #sql will holde the sql statement
            sql = ''
            
            # waiting is if we are waiting to see a ';' to indicate the statement end.
            waiting = False
            for line in open('/Users/Luis Garcia/OneDrive/Desktop/cs491/project_1/sql/university.sql'):
                print("File was oppened")
                # Strip the line of the new line character, '\n'
                line = line.strip()

                # Is this just an empty line?
                if line == '':
                    # Yep, move on.
                    continue
                elif line[0] == '-' or line[0] == '/':
                    # We have a comment here, move on
                    continue
                elif line[len(line)-1] == ';' and waiting:
                    # We've been waiting for the end of statement character, ';'
                    # and now we've found it
                    waiting = False         # Set waiting to false
                    sql = sql + line        # Add the last line to the statement
                    print(sql)              # Output the statement to the terminal
                    cursor.execute(sql)     # Execute the statement
                    sql = ''                # Reset our sql variable
                    continue                # Move on with the for loop
                elif len(line) > 6:
                    # Is the length of the line > 6 (since we want to check up to index 5)?
                    if line[0] == 'C' and line[1] == 'R' and line[2] == 'E' and line[3] == 'A' and line[4] == 'T' and line[5] == 'E':
                        # Yep, did the first 5 char spell create? Yep!
                        # We're making a new table then
                        waiting = True      # Set waiting to true.
                        sql = sql + line    # Add the line to the sql variable
                        continue            # Move on with the for loop
                    elif waiting:
                        # The length is indeed longer, but we're not a create statement
                        # and we are waiting to be executed
                        sql = sql + line    # Add the line to the sql variable
                        continue            # Move on with the for loop
                    else:
                        # The length is indeed longer, but we're not waiting either
                        # Print and execute the command and continue on
                        print('Here')
                        print(line)
                        cursor.execute(line)
                        continue
                elif waiting:
                    # None of the above are true, but we're waiting
                    sql = sql + line        # Add the line to the sql variable
                    continue                # Move on with the for loop
                # Nothing above was true, and we're not waiting for an ';'
                # Print the command and execute it.
                print('Here')
                print(line)
                cursor.execute(line)
            # Create our response to the client and return it
            # message = {
            #     'status': 200,
            #     'message': 'Database successfully initialized!',
            # }
            # response = jsonify(message)
            # response.status_code = 200
            # return response
            flash('Database created', category='success')
        except Exception as e:
            # Was there some error in our code above?
            # Print it out to the terminal so we can try and debug it
            print(e)
        finally:
            if rejected == False:
                # If we've made it here, then we successfully executed out try
                # Now we can close our cursor and connection
                cursor.close()
                # conn.close()

    return render_template('initialize_db.html', user=current_user)

@views.route("/upload-picture", methods=['GET', 'POST'])
@login_required
def uploadPic():
    
    return render_template('pic.html', user=current_user)
