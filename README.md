
# SimpleNLP: medical condition detection in clinical text

* Code acompaining paper:[] 
* Web API version can be found at https://hit.nyumc.org/simpleNLP.

# Data:
* Any text data can be used

## 1. System requirements 
* software dependencies python3, textblob

## 2. Installation guide
* Instructions
Clone this repo to your local machine using:
```
 git clone https://github.com/sedab/SimpleNLP
 
```
*run: 
** python -m textblob.download_corpora
** pip install textblob

* Typical install time on a "normal" desktop computer is around 10 seconds.

## 3. Demo
The user needs to define the configurations ( Tuned mi, stroke, pe, dvt, other thrombosis event configuration files are given in Config folder)

* Target phrases are the list of terms that describe the clinical entity in question, such as "embolus" or "thromboembolism." When a target phrase is found within a report, the tool checks to see whether the target phrase is negated (e.g. “no evidence of embolus”). If the tool finds more sentences that contain the target phrase than negate the target phrase, the report is scored as "present", otherwise it is scored as "absent". In cases of a tie, the report is scored as "present" but marked as ambiguous.

* Skip phrases are used to eliminate sentences in the narrative that might confuse the classifier; this is useful for situations in which the target phrase is contained within the indications section of the report (e.g. "Indication for study: concern for PE").

* The start phrase allows the user to specify where within the report to start the analysis. Specifying a start phrase is useful if the report contains a "conclusion" or "impression" section, as the tool can then be focused only on a subset of the report. If the start phrase is not found or not chosen, the classifier starts at the beginning of the report.

* Absolute asssertions allow you to enter phrases that if found in the text will override all other logic and mark the case as either "present" or "absent".

### iPython Notebooks

* ```Test.ipynb``` demonstrates the usage of the tool

