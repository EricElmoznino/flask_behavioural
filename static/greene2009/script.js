let debug = false;

/* Parameters */
let rootPath = "https://ee.cognitivestudies.online/";
if (debug) {
    rootPath = "http://127.0.0.1:5000/";
}

/* Globals */
var trials = [];
var curTrial = 0;
var curResponse = null;
var nTraining;
var trialStartTime;
var experimentStartTime;
var training = true;
var canProceed = true;

/* Responses */
var responses = [];
var responseHands = [];
var posImages = [];
var negImages = [];
var conditions = [];
var reactionTimes = [];

function trialDone() {
    if (!training) {
        trial = trials[curTrial];

        // Record the response and information about the trial
        responses.push(trial["optionOrder"][curResponse]);
        responseHands.push(curResponse === 1 ? "right" : "left");
        posImages.push(trial["images"][0]);
        negImages.push(trial["images"][1]);
        conditions.push(trial["condition"]);
        reactionTimes.push((new Date()) - trialStartTime);
    }

    if (curTrial === nTraining - 1) {
        training = false;
    }

    curTrial++;

    // Finished experiment
    if (curTrial >= trials.length) {
        doneExperiment();
        return;
    }

    curResponse = null;
    trialBegin();
}

function trialBegin() {
    trialStartTime = new Date();
    $("#trialImg1").prop("src", trials[curTrial]["images"][0]);
    $("#trialImg2").prop("src", trials[curTrial]["images"][1]);
}

function finishedTraining() {
    canProceed = false;
    $("#trainEndWarning").show();
    $("#proceedExperiment").click(function () {
        canProceed = true;
        $("#trainEndWarning").hide();
        $("#nextTrialMessage").show();
    });
}

function doneExperiment() {
    $.ajax({
        url: rootPath + "post_responses",
        type: "POST",
        data: JSON.stringify({
            "Response": responses, "Response Hand": responseHands,
            "Positive Image": posImages, "Negative Image": negImages,
            "Condition": conditions, "Reaction Time": reactionTimes,
            "Experiment Time": new Date() - experimentStartTime
        }),
        dataType: "json",
        contentType: "application/json",
        success: function (response) {
            console.log("testing123");
            $("#trial").hide();
            $(document).unbind("keydown.responded");
            $(document).unbind("keydown.nextTrial");
            // todo: Display a thank you message
            // todo: Take the participant back to Prolific (maybe after they press some button)
        },
        error: e => console.log(e)
    });
}

function startExperiment() {
    experimentStartTime = new Date();
    $("#instructionsContainer").hide();
    $("#trial").show();

    // Keyboard events

    // User has selected a response (pressed a key)
    $(document).bind("keydown.responded", function (event) {
        // Check if the key corresponds to a valid response
        if (event.which != 70 && event.which != 74) {
            return;
        }

        // If this is the last training image, give a warning that must be acknowledged before continuing
        if (curTrial === nTraining - 1 && curResponse === null) {
            finishedTraining();
        }

        // Allow user to continue to the next trial
        if (canProceed) {
            $("#nextTrialMessage").show();
        }

        // Register which response was made
        if (event.which == 70) {
            curResponse = 0;
            $("#option1box").css("background-color", "lightgrey");
            $("#option2box").css("background-color", "white");
        } else {
            curResponse = 1;
            $("#option2box").css("background-color", "lightgrey");
            $("#option1box").css("background-color", "white");
        }
    });

    // User wishes to continue to the next trial (pressed the "Space" key)
    $(document).bind("keydown.nextTrial", function (event) {
        // Check if they pressed the space bar and that they"ve responded
        // (and that they"ve acknowledged being done training)
        if (event.which == 32 && curResponse != null && canProceed) {
            $("#nextTrialMessage").hide();
            $("#option1box").css("background-color", "white");
            $("#option2box").css("background-color", "white");
            if (curTrial === nTraining - 1) {                   // If training has ended
                $("#sessionMode").html("Experiment segment")
            }
            trialDone();
        }
    });

    trialBegin();
}

/* Setup/preloading code */

function getTrials(callback) {
    $.ajax({
        url: rootPath + "get_trials",
        type: "GET",
        success: function (response) {
            var trainTrials = response["trials"]["train"];
            var testTrials = response["trials"]["test"];
            nTraining = trainTrials.length;
            trials = trainTrials.concat(testTrials);
            callback();
        },
        error: e => console.log(e)
    });
}

$(document).ready(function () {
    $("#trial").hide();
    getTrials(function () {
        $("#startExperiment").click(function () {
            if ($("#consent").prop("checked") === false) {
                return;
            }
            startExperiment();
        });
    });
});
