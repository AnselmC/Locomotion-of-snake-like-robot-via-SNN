(defconst sli-docdir "/home/christoph/nest-simulator-2.14.0/share/doc/nest")
(defconst sli-datadir "/home/christoph/nest-simulator-2.14.0/share/nest")
(defconst sli-sourcedir "/home/christoph/nest-simulator-2.14.0-src")

(setq load-path (cons (concat sli-datadir "/extras/emacs") load-path))

(defvar running-xemacs (string-match "XEmacs\\|Lucid" emacs-version))

(provide 'sli)
(require 'postscript-sli)
(require 'easymenu)
(require 'psvn)
(cond (running-xemacs (require 'func-menu)))
	
(setq svn-trac-project-root "http://nest-initiative.org/trac/")

;; NOTE: all functions defined in this file start with "sli-".


;(autoload 'postscript-mode "postscript" "SLI Mode" t)
;(setq auto-mode-alist (cons '("\\.sli\\'" . postscript-sli-mode) auto-mode-alist))
(setq auto-mode-alist (cons '("\\(\\.sli\\|\\.hlp\\)" . postscript-sli-mode) auto-mode-alist))


(message "Installing SLI postscript extention...")

(defcustom sli-command (list "nest" "-")
  "*Command used to invoke a SLI shell."
  :group 'sli
  :type 'list
  )

(defcustom sli-shell-prompt-pattern "^SLI .*\\] "
  "*Regular expression to match the SLI prompt."
  :group 'sli
  :type 'string
 )

;; --Add Menus - using easymenu.el--
;; (see "describe-function easy-menu-define" for details!)

(defvar sli-mode-edit-menu-def
  '("SLI edit"
;;; not working with Emacs:        ["Jump to documented function in this buffer" fume-list-functions t]
;     ("Insert code template"
      ["Code template: Documentation header" sli-insert-doc-header t]
      "--"
      ["Code template: Function (simple)" sli-insert-simple-function t]
      ["Code template: Function (trie)" sli-insert-trie-function t]
      ["Code template: Function (wrapper)" sli-insert-wrapper-function t]
      "--"
      ["insert template: Case statement" sli-to-do nil]
      ["insert template: For statement" sli-to-do nil]
;      )
     )
   )

(defvar sli-mode-shell-menu-def
  '("SLI shell"
    ["Start SLI shell" sli-shell t]
    "--"
    ["Execute string" sli-execute-string t]
    ["Execute region" sli-execute-region t]
    ["Execute buffer" sli-execute-buffer t]
    "--"
    ["Edit ~/.nestrc" sli-edit-nestrc t]
     )
   )

(defvar sli-mode-help-menu-def
 '("SLI help"
   ["Help on command" sli-help-command t]
   ["Help on highlighted command" sli-help-region t]
   ["Show index of commands (text)" sli-helpindex-text t]
   "-"
   ["Browse index of commands (default browser)" sli-helpindex-default t]
;   ["Browse index of commands (Firefox)" sli-helpindex-firefox t]
;   ["Browse index of commands (KDE)" sli-helpindex-kde t]
;   ["Browse index of commands (W3)" sli-helpindex-w3 t]
;   "-"
   ["Browse helpdesk (default browser)" sli-helpdesk-default t]
;   ["Browse helpdesk (Firefox)" sli-helpdesk-firefox t]
;   ["Browse helpdesk (KDE)" sli-helpdesk-kde t]
;   ["Browse helpdesk (W3)" sli-helpdesk-w3 t]
;   "-"
   ["Browse nest-initiative homepage (default browser)" sli-nestinitiative-default t]
;   ["Browse nest-initiative homepage (Firefox)" sli-nestinitiative-firefox t]
;   ["Browse nest-initiative homepage (KDE)" sli-nestinitiative-kde t]
;   ["Browse nest-initiative homepage (W3)" sli-nestinitiative-w3 t]
   "-"
   ["Set your default browser" (customize-variable 'browse-url-browser-function) t]
   )
 )

(defvar sli-mode-developer-menu-def
 '("NEST Trac"
   [(concat "SVN status " sli-sourcedir) sli-svn-status t]
   "-"
   ["Browse wiki" svn-trac-browse-wiki t]
   ["Browse timeline" svn-trac-browse-timeline t]
   ["Browse roadmap" svn-trac-browse-roadmap t]
   ["Browse source" svn-trac-browse-source t]
   ["Browse report" svn-trac-browse-report t]
   ["Browse ticket" svn-trac-browse-ticket t]
   ["Browse changeset" svn-trac-browse-changeset t]
   ["Set Trac project root" svn-status-set-trac-project-root t]
;   ["Browse NEST Trac (default browser)" sli-trac-default t]
;   ["Browse NEST Trac (Firefox)" sli-trac-firefox t]
;   ["Browse NEST Trac (KDE)" sli-trac-kde t]
;   ["Browse NEST Trac (W3)" sli-trac-w3 t]
   "-"
   ["Set your default browser" (customize-variable 'browse-url-browser-function) t]
   )
 )

;; add keybindings to the postscript-sli keymap (was initialized by postscript-sli.el, which is rquired above):
(define-key ps-sli-mode-map [(control c) (control s)] 'sli-shell)
(define-key ps-sli-mode-map [(control c) (control b)] 'sli-execute-buffer)
(define-key ps-sli-mode-map [(control c) (control r)] 'sli-execute-region)
(define-key ps-sli-mode-map [(control c) (\?)] 'sli-help-region)

;; and add menues to it:
(easy-menu-define unused ps-sli-mode-map "doc unused" sli-mode-developer-menu-def)
(easy-menu-define unused ps-sli-mode-map "doc unused" sli-mode-help-menu-def)
(easy-menu-define unused ps-sli-mode-map "doc unused" sli-mode-edit-menu-def)
(easy-menu-define unused ps-sli-mode-map "doc unused" sli-mode-shell-menu-def)

;; the following does not work equally with Emacs and XEmacs, so we better refrain from it...
;;;; and we add the Shell menu to the global map:
;;(easy-menu-define unused global-map "doc unused" sli-mode-shell-menu-def)


;; -- add sli hook to the postscript-sli hooklist--
(add-hook 'ps-sli-mode-hook 'sli-install-sli)
;; -- end add sli hook to the postscript-sli hooklist--

(message "Installing SLI postscript extention...done")





;; function definitions below

;; --define sli hook--  
(defun sli-install-sli ()
  ;;  (interactive)

; Required for the menus to actually appear in XEmacs (not required for Emacs):
; (See the documentation file easymenu.el in your XEmacs installation.)
; (Note: The Emacs installation often contains not the original
;  easymenu.el, but a lightweight compatibility version.)
(easy-menu-add sli-mode-shell-menu-def)
(easy-menu-add sli-mode-edit-menu-def)
(easy-menu-add sli-mode-help-menu-def)
(easy-menu-add sli-mode-developer-menu-def)

   ;; --End: Add Menus--

   ;; --turn on function menu:--
;;;(cond (running-xemacs  (fume-add-menubar-entry)))
(cond (running-xemacs  (turn-on-fume-mode)))
   ;; --End: turn on function menu:--

)


;; for the execute functions, you might also want to have a look in
;; the commented-out implementations in postscript-sli.el. Ruediger 10-aug-2007
(defun sli-execute-buffer ()
  "Send contents of the buffer for execution to the SLI shell.
If no SLI shell process is running, a SLI new shell is started."
  (interactive)
  (save-excursion
    (mark-whole-buffer)
    (sli-execute-region (point-min) (point-max))))

(defun sli-execute-region (start end)
  "Send the region between START and END for execution to the SLI shell.
If no SLI shell process is running, a SLI new shell is started."
  (interactive "r")
  (let ((start (min (point) (mark)))
	(end (max (point) (mark))))
    
    ;; store the command to execute in sli-command-string:
    (setq sli-command-string (buffer-substring start end)) 

        (sli-execute-string sli-command-string)
    ))

(defun sli-execute-string (command)
  "Send the string for execution to the SLI shell.
If no SLI shell process is running, a SLI new shell is started."
  (interactive "sCommand: ")
  ;; This is what is really sent:
  ;; We return to batch mode by sending "exit", in order not to have
  ;; the prompt printed after every command. 
  ;; We prepend "() =" to the command string in order to have the
  ;; result of the command printed on a new line.
  ;; We append "\n" in case the region does not end with a newline.
  ;; We return to interactive mode by sending "executive".

;     (condition-case nil
;         (process-send-string "SLI" "exit\n")
;       (error
;       (sli-shell)
;       (process-send-string "SLI" "exit\n")
;       )
;      )

       (condition-case nil
           (process-send-string "SLI" "() =\n")
         (error
          (sli-shell)
          (process-send-string "SLI" "() =\n")
          )
         )
    (process-send-string "SLI" (concat command "\n"))
;;    (process-send-string "SLI" "executive\n")

  )


(defun sli-shell ()
  "Start a shell communicating with a SLI Interpreter."
  (interactive)
  (require 'shell)
  (switch-to-buffer-other-window
    (apply 'make-comint
           "SLI"
           (car sli-command)
           nil
           (cdr sli-command)))
  (setq comint-prompt-regexp sli-shell-prompt-pattern)
  (process-send-string "SLI" "executive\n")
  )


(defun sli-insert-doc-header ()
  "Insert the SLI documentation header template."
  (interactive)
  (insert-file (concat sli-docdir "/doc_header.txt"))
)

(defun sli-edit-nestrc ()
  "Edit the user's .nestrc file."
  (interactive)
  (find-file (concat (getenv "HOME") "/.nestrc"))
)

(defun sli-svn-status ()
  (interactive)
  (require 'psvn)
  (svn-status sli-sourcedir)
  )




;; --function for making templates--
;; -- (taken from the nase.el file) --

;; Statement templates. This is taken from the idlwave.el file,
;; with small modifications (no case changes are done, and no
;; new line is opened).
;; A comment in the idlwave.el file said:
;;   "Replace these with a general template function, something like
;;    expand.el (I think there was also something with a name similar to
;;    dmacro.el)"

(defun sli-template (s1 s2 &optional prompt noindent)
  "Build a template with optional prompt expression.

This is the SLI version of the idlwave-template function. It differs
only in that no case changes are done, and no new line is opened.
In addition, it handles a possible active region in the way that is expected.

S1 and S2 are strings.  S1 is inserted at point followed
by S2.  Point is inserted between S1 and S2. If optional argument
PROMPT is a string then it is displayed as a message in the
minibuffer.  The PROMPT serves as a reminder to the user of an
expression to enter.

The lines containing S1 and S2 are reindented using `indent-region'
unless the optional second argument NOINDENT is non-nil."
;   (cond ((eq idlwave-abbrev-change-case 'down)
;	 (setq s1 (downcase s1) s2 (downcase s2)))
;	(idlwave-abbrev-change-case
;	 (setq s1 (upcase s1) s2 (upcase s2))))
  (let ((beg (save-excursion (beginning-of-line) (point)))
        end)
    ;(if (not (looking-at "\\s-*\n"))
    ;    (open-line 1))

    (if (not (region-active-p))
        ;;then (one expression only!)
        (insert s1)
      ;;else (n expressions)
      (save-excursion
        (goto-char (region-beginning))
        (insert s1)
        )
      )

    (save-excursion
      (insert s2)
      (setq end (point)))
    (if (not noindent)
        (indent-region beg end nil))
    (if (stringp prompt)
        (message prompt))))

;--End: function for making templates--


;; --templates--
(defun sli-insert-simple-function (name)
  (interactive "sRoutine name: ")
  (sli-template
   (concat (concat "/" name) "\n{\n")
   "\n} bind def"
   "Insert code." nil))

(defun sli-insert-trie-function (name)
  (interactive "sRoutine name: ")
  (sli-template
   (concat (concat "/" name) "[/")
   "type]\n{\n\n} bind def"
   "Specify operand types here:  /integertype /doubletype /..." nil))

(defun sli-insert-wrapper-function (name)
  (interactive "sRoutine name: ")
  (sli-template
   (concat (concat "/" name) "[/")
   "type /]\n{\n\n} SLIFunctionWrapper"
   "Specify parameter list here:  /integertype /i  /doubletype /d  /... /..." nil))




;; --(even more) experimental functions--
(defun sli-process-single-result (proc res)
  (setq sli-single-result res)
)
(defun sli-tellme (command)
  (interactive "sCommand: ")

  ;; start a shell, if non is running:
    (condition-case nil
        (process-send-string "SLI" " ")
      (error
       (sli-shell)
       )
      )
 
  ;; keep old process filter in mind:
  (setq sli-process-filter (process-filter (get-process "SLI")))

  (set-process-filter (get-process "SLI") 'sli-process-single-result)
  
  (process-send-string "SLI" (concat command " =\n") )
;;  (sli-execute-string command)

  (accept-process-output (get-process "SLI") )

  ;; reset old process filter:
  (set-process-filter (get-process "SLI") sli-process-filter)

  ;; return value:
  sli-single-result
)


(defun sli-helpindex-text ()
  (interactive)
  (view-file-other-window (concat sli-docdir "/help/helpindex.hlp"))
  )
(defun sli-helpindex-default ()
  (interactive)
  (browse-url (concat "file:" sli-docdir "/help/helpindex.html"))
  )
(defun sli-helpindex-firefox ()
  (interactive)
  (browse-url-firefox (concat "file:" sli-docdir "/help/helpindex.html"))
  )
(defun sli-helpindex-kde ()
  (interactive)
  (browse-url-kde (concat "file:" sli-docdir "/help/helpindex.html"))
  )
(defun sli-helpindex-w3 ()
  (interactive)
  (browse-url-w3 (concat "file:" sli-docdir "/help/helpindex.html"))
  )

(defun sli-help-command (command)
  (interactive "sCommand: ")

  ;; the help file might be in the cc or the sli subdirectory. We will check both.
  (let (
        (cc-filename  (concat sli-docdir "/help/cc/" command ".hlp"))
        (sli-filename (concat sli-docdir "/help/sli/" command ".hlp"))
        )

    (message cc-filename)
    
    (if (file-exists-p cc-filename) (view-file-other-window cc-filename)
      (if (file-exists-p sli-filename) (view-file-other-window sli-filename)
        (message (concat "No help information found for command " command))
        )
      )
    )
  )

(defun sli-help-region (start end)
  (interactive "r")
    
    (sli-help-command (buffer-substring start end)) 
  )

(defun sli-helpdesk-default ()
  (interactive)
  (browse-url (concat "file:" sli-docdir "/index.html"))
  )
(defun sli-helpdesk-firefox ()
  (interactive)
  (browse-url-firefox (concat "file:" sli-docdir "/index.html"))
  )
(defun sli-helpdesk-kde ()
  (interactive)
  (browse-url-kde (concat "file:" sli-docdir "/index.html"))
  )
(defun sli-helpdesk-w3 ()
  (interactive)
  (browse-url-w3 (concat "file:" sli-docdir "/index.html"))
  )

(defun sli-nestinitiative-default ()
  (interactive)
  (browse-url "http://www.nest-initiative.uni-freiburg.de")
  )
(defun sli-nestinitiative-firefox ()
  (interactive)
  (browse-url-firefox "http://www.nest-initiative.uni-freiburg.de")
  )
(defun sli-nestinitiative-kde ()
  (interactive)
  (browse-url-kde "http://www.nest-initiative.uni-freiburg.de")
  )
(defun sli-nestinitiative-w3 ()
  (interactive)
  (browse-url-w3 "http://www.nest-initiative.uni-freiburg.de")
  )

(defun sli-trac-default ()
  (interactive)
  (browse-url "http://www.nest-initiative.uni-freiburg.de/cgi-bin/trac.cgi")
  )
(defun sli-trac-firefox ()
  (interactive)
  (browse-url-firefox "http://www.nest-initiative.uni-freiburg.de/cgi-bin/trac.cgi")
  )
(defun sli-trac-kde ()
  (interactive)
  (browse-url-kde "http://www.nest-initiative.uni-freiburg.de/cgi-bin/trac.cgi")
  )
(defun sli-trac-w3 ()
  (interactive)
  (browse-url-w3 "http://www.nest-initiative.uni-freiburg.de/cgi-bin/trac.cgi")
  )



 ;; -------- support for function menu ------------
(cond (running-xemacs  

;;(defvar fume-function-name-regexp-idlwave
;;  (cons "^\\s *\\([pP][rR][oO]\\|[fF][uU][nN][cC][tT][iI][oO][nN]\\)\\s +\\([A-Za-z][A-Za-z0-9_$]*\\(::[A-Za-z][A-Za-z0-9_$]*\\)?\\)" 2)
;;  "Expression to get SLI function names.")

;(defun fume-find-next-idlwave-function-name (buffer)
;  "Search for the next IDL function in BUFFER."
;  (set-buffer buffer)
;  (if (re-search-forward (car fume-function-name-regexp-idlwave) nil t)
;      (let ((beg (match-beginning (cdr fume-function-name-regexp-idlwave)))
;            (end (match-end (cdr fume-function-name-regexp-idlwave))))
;        (cons (buffer-substring beg end) beg))))

(defvar fume-function-name-regexp-sli
;;  (cons "^\\s *Name:\\s *\\(\\(:\\|::\\)?[_a-zA-Z0-9\\-]+::\\)\\(\\(:\\|::\\)?[_a-zA-Z0-9\\-]+\\)" 2)
  (cons "^\\s-*Name:\\s-*\\([_a-zA-Z0-9:\\-]+\\)" 1)
;; to search for def-constructs, we probably need balanced expression matching (sexp). Won't do that now...
;;;;;  (cons "\\/\\([_a-zA-Z0-9:\\-]+\\).*{.*}.*\\(def\\|SLIFunctionWrapper\\)" 1)
;; Ruediger
  "Expression to get SLI function names.")

(defun fume-find-next-sli-function-name (buffer)
  "Search for the next SLI function in BUFFER."
  (set-buffer buffer)
  (if (re-search-forward (car fume-function-name-regexp-sli) nil t)
      (let ((beg (match-beginning (cdr fume-function-name-regexp-sli)))
            (end (match-end (cdr fume-function-name-regexp-sli))))
        (cons (buffer-substring beg end) beg))))

(setq fume-function-name-regexp-alist
      (cons '(postscript-sli-mode . fume-function-name-regexp-sli)
            fume-function-name-regexp-alist))

(setq fume-find-function-name-method-alist
      (cons '(postscript-sli-mode . fume-find-next-sli-function-name)
            fume-find-function-name-method-alist))

;(defvar fume-function-name-regexp-c++
;  (cons
;   (concat
;    "\\(\\`\\|[^\\]\n\\)" ; avoid matching on last line of macro definition
;    "\\(#define\\s-+\\|"
;    "\\(template\\s-+<[^>]+>\\s-+\\)?"           ; template formals
;    "\\([a-zA-Z0-9_*&<,>:]+\\s-+\\)?"            ; type specs; there can be no
;    "\\([a-zA-Z0-9_*&<,>\"]+\\s-+\\)?"           ; more than 3 tokens, right?
;    "\\([a-zA-Z0-9_*&<,>]+\\s-+\\)?\\)"
;    "\\(\\([a-zA-Z0-9_&~:<,>*]\\|\\(\\s +::\\s +\\)\\)+\\)"
;    "\\(o?perator\\s *.[^(]*\\)?\\(\\s-\\|\n\\)*(" ; name
;    ) 7)
;  "Expression to get C++ function names.")

)) ;; matches: (cond (running-xemacs
;; -------- end: support for function menu ------------


;; ==================================================================




