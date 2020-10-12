
        function changefolder(i) {
            y = document.getElementById('change_folder')
            y.value = i
            y.click()
        }

        function folderpopup(){
            i = document.getElementById('popupfolder');
            y = document.getElementById('popupfile');
            yy = document.getElementById('popupfolders');
            if (getComputedStyle(y, null).display == 'none' || getComputedStyle(yy, null).display == 'none'){
                display = getComputedStyle(i, null).display;
                if (display == 'none'){
                    i.style.display = 'block';
                } else {
                    i.style.display = 'none';
                }
            }else{
                i.style.display = 'block';
                y.style.display = 'none';
                yy.style.display = 'none';
            }
        }
        // Get the input field
        var input = document.getElementById("newfoldername");

        // Execute a function when the user releases a key on the keyboard
        input.addEventListener("keyup", function(event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.keyCode === 13) {
            // Cancel the default action, if needed
            event.preventDefault();
            // Trigger the button element with a click
            document.getElementById("submitfolder").click();
        }
        });

        function filepopup(){
            i = document.getElementById('popupfile');
            ii = document.getElementById('popupfolders');
            y = document.getElementById('popupfolder');
            if (getComputedStyle(y, null).display == 'none'){
                display = getComputedStyle(i, null).display;
                if (display == 'none'){
                    i.style.display = 'block';
                    ii.style.display = 'block';
                } else {
                    i.style.display = 'none';
                    ii.style.display = 'none';
                }
            } else{
                i.style.display = 'block';
                ii.style.display = 'block';
                y.style.display = 'none';
            }
        }
        function fileuploaded(){
            document.getElementById('submitfile').click()
        }
        function foldersuploaded(){
            document.getElementById('submitfolders').click()
        }

        function deleteItem(i){
            let y = document.getElementById('delete_button')
            console.log(y)
            y.value = i;
            let x = confirm('Delete ' + i + " ?")
            if (x == true){
                y.click()
            }
        }
        function editItem(i){
            let y = document.getElementById('edit_button')
            console.log(y)
            let x = prompt('Assign a new name for ' + i)

            if (!x == null || !x == ''){
                y.value = String(i + "," + x)
                y.click();
            }
        }
        function download_folder(i){
            let y = document.getElementById('zip_folder');
            console.log(y);
            y.value = i;
            y.click();
            console.log(y.value);
        }


        function deleteItem(i){
            let y = document.getElementById('delete_button')
            console.log(y)
            y.value = i;
            let x = confirm('Delete ' + i + " ?")
            if (x == true){
                y.click()
            }
        }

        function editItem(i){
            let y = document.getElementById('edit_button')
            console.log(y)
            let x = prompt('Assign a new name for ' + i)

            if (!x == null || !x == ''){
                y.value = String(i + "," + x)
                y.click();
            }
        }

        function fileuploaded(){
            document.getElementById('submitfile').click()
        }