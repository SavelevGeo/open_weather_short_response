import tkinter as tk
import tkinter.ttk as ttk
import weather_request

root= tk.Tk()
root['background'] = '#BADCED'

coordsLabel = ttk.Label(
						root,
						text = 'lat, lon',
						background = root['background'], 
						foreground = '#273273'
						)
coordsLabel.grid(
				row = 0,
				column = 0,
				columnspan = 2, 
				pady = (20,0) 
				)

coordsVar = tk.StringVar()
coordsEntry = ttk.Entry(
						root,
						textvariable = coordsVar, 
						)

coordsEntry.grid(
				row = 1,
				column = 0,
				columnspan = 2,
				pady = (0,20)
				) 

def is_clipboard_empty(): #(c) Reblochon Masque 
    try:
        root.selection_get(selection="CLIPBOARD")
    except tk.TclError:    # error raised when empty
        return True
    return False 

def pasteSelection():
	if not is_clipboard_empty():
		coordsVar.set(root.clipboard_get()) 
		
coordsPasteButton = ttk.Button(
								root, 
								text = 'paste from clipboard', 
								command = pasteSelection
								)

coordsPasteButton.grid(row = 2, column = 0)

coordsClearButton = ttk.Button(
								root,
								text = 'clear',
								command = lambda :
								coordsVar.set('')
								)

coordsClearButton.grid(row = 2, column = 1)

def pasteRequest():
	resultText.delete('1.0', 'end')
	if ',' in coordsVar.get():
		resultText.insert(
							tk.INSERT,
							weather_request.req(
												coordsVar.get(),
												test = False,
												)
						  )
									   
requestButton = ttk.Button(
							root,
							text = 'request',
							command = pasteRequest
							)

requestButton.grid(row = 3, column = 0, columnspan = 2)

resultText = tk.Text(
					root,
					width = 20, 
					height = 7, 
					wrap = tk.WORD,
					padx = 20,
					pady = 20
					)
resultText.grid(
				row = 4,
				column = 0,
				columnspan = 2, 
				sticky = 'n'
				)

def copyRequest():
	reqText = resultText.get('1.0', 'end')
	root.clipboard_clear()
	root.clipboard_append(reqText)
	
copyRequest = ttk.Button(
						root,
						text = 'copy to clipboard', 
						command = copyRequest
						)
											  
copyRequest.grid(
				row = 5,
				column = 0,
				columnspan = 2, 
				sticky = 'n'
				)

root.grid_columnconfigure(0, weight = 1)
root.grid_columnconfigure(1, weight = 1)
root.grid_rowconfigure(0, weight = 0)
root.grid_rowconfigure(1, weight = 0)
root.grid_rowconfigure(2, weight = 0)
root.grid_rowconfigure(3, weight = 2)
root.grid_rowconfigure(4, weight = 1)
root.grid_rowconfigure(5, weight = 2)
root.mainloop()