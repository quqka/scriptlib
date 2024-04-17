import os
import maya.cmds as cmds
from PySide2.QtWidgets import QScrollArea, QLineEdit, QPushButton, QGridLayout, QLabel, QFileDialog, QRadioButton
from PySide2.QtCore import Qt

class RefWindow(QScrollArea):
    def __init__(self, parent=None):
        super(RefWindow, self).__init__(parent)
        ref_node = cmds.ls('*RN*', type="reference", r=True)
        self.ref_path_dict = {}
        self.ref_node_dict = {}

        for ref in ref_node:
            try:
                if not cmds.referenceQuery(ref, isLoaded=True):
                    continue
                ref_path = cmds.referenceQuery(ref, f=True)
                self.ref_path_dict[ref_path] = ""
                self.ref_node_dict[ref_path] = ref
            except Exception as e:
                cmds.warning(e)

        self.initUI()
        
    def initUI(self):
        self.setGeometry(500, 300, 400, 270)
        self.setWindowTitle("Batch Reference")
        layout = QGridLayout()
        ref_index = 0
        for key, value in self.ref_path_dict.items():
            self.createPartWidget(layout, ref_index, key, value)
            ref_index += 1
        submitButton = QPushButton()
        submitButton.setText("Submit")
        submitButton.clicked.connect(self.onSubmitClicked)
        layout.addWidget(submitButton, ref_index, 2)   
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
    
    def createPartWidget(self, layout, index, key, value):
        selectRadio = QRadioButton()
        selectRadio.toggled.connect(lambda: cmds.select(cmds.referenceQuery(key, nodes=True)))
        layout.addWidget(selectRadio, index, 0)
        
        oldEdit = QLineEdit()
        oldEdit.setText(key)
        oldEdit.setReadOnly(True)
        oldEdit.setFocusPolicy(Qt.NoFocus)
        layout.addWidget(oldEdit, index, 1)
        
        oldButton = QPushButton()
        oldButton.clicked.connect(lambda: QFileDialog.getOpenFileName(self, "SelectFile", key,"All Files (*)", options=QFileDialog.Options()))
        layout.addWidget(oldButton, index, 2)
        
        label = QLabel()
        label.setText("===")
        layout.addWidget(label, index, 3)
        
        newEdit = QLineEdit()
        newEdit.setText(value)
        newEdit.textChanged.connect(lambda text:self.onNewTextChanged(text, key))
        
        layout.addWidget(newEdit, index, 4)
        newButton = QPushButton()
        newButton.clicked.connect(lambda: newEdit.setText(QFileDialog.getOpenFileName()[0]))
        layout.addWidget(newButton, index, 5)
        
    def onNewTextChanged(self, text, key):
        self.ref_path_dict[key] = text
        
    def onSubmitClicked(self):
        for key, value in self.ref_path_dict.items():
            if not value:
                continue
            if not os.path.exists(value):
                continue
            
            cmds.file(value, loadReference=self.ref_node_dict[key])       
        
rwindow = RefWindow()
rwindow.show()
