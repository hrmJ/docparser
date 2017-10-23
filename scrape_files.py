# Hae ubuntun manuaalisivuilta monikielistä dataa ja tee niistä käännösmuisti
from clusters import MultiLangDocu


MyDocu = MultiLangDocu(["fi","en","de","fr","ru","sv"])
for theme in ["net-wireless","files","clock","prefs-language","prefs-display","media","accounts","shell-overview","tips","a11y","printing","bluetooth","color","keyboard","mouse","power"]:
    print("STARTING " + theme)
    MyDocu.GetFilesFromCluster(theme)
